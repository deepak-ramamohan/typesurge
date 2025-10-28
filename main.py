import arcade
from space_shooter.views import SpaceShooterGameView
from ai_trainer.ai_trainer import AITrainerView
from utils.menu_view import MenuView
from utils.resources import USER_PROFILE_SPRITE
from utils.colors import BROWN
from arcade.gui import UIFlatButton, UIImage
from utils.button_styles import transparent_button_style
from utils.user_profile import UserProfile


class MainMenuView(MenuView):

    def __init__(self):
        title_text = "Welcome to TypeMania!"
        self.TITLE_OFFSET_FROM_CENTER = 75
        self.SUBTITLE_OFFSET_FROM_TITLE = -10
        self.TITLE_FONT_SIZE = 78
        self.BUTTON_OFFSET_FROM_SUBTITLE = -50
        super().__init__(
            title_text=title_text,
            subtitle_text=""
        )
        space_shooter_button = self.create_button("Space Shooter")
        @space_shooter_button.event("on_click")
        def _(event):
            self._start_game()

        ai_trainer_button = self.create_button("AI Trainer")
        @ai_trainer_button.event("on_click")
        def _(event):
            self._start_ai_trainer()
 
        quit_button = self.create_button("Quit")
        @quit_button.event("on_click")
        def _(event):
            self._quit_game()

        self.initialize_buttons(
            [
                space_shooter_button,
                ai_trainer_button,
                quit_button
            ]
        )

        self.main_menu_music = arcade.Sound("assets/sounds/hard_boiled.mp3", streaming=True)
        self.current_music = arcade.play_sound(self.main_menu_music, loop=True)

        self._initialize_user_profile()
        
    def _initialize_user_profile(self):
        self.user_profiles = [
            UserProfile(name="user_1", display_name="User 1"),
            UserProfile(name="user_2", display_name="User 2"),
            UserProfile(name="user_3", display_name="User 3")
        ]
        self.user_index = 0
        BUTTON_SIZE = 45
        user_profile_button = UIFlatButton(
            text="",
            x=15,
            y=10,
            height=BUTTON_SIZE,
            width=BUTTON_SIZE,
            style=transparent_button_style
        )
        user_profile_button.add(
            child=UIImage(
                texture=USER_PROFILE_SPRITE,
                width=BUTTON_SIZE - 3,
                height=BUTTON_SIZE - 3
            )
        )
        user_profile_text = arcade.Text(
            text=self.user_profiles[self.user_index].display_name, 
            x=user_profile_button.right + 10,
            y=user_profile_button.center_y,
            anchor_x="left",
            anchor_y="center",
            font_name=self.FONT_NAME,
            font_size=32,
            batch=self.text_batch,
            color=BROWN
        )
        @user_profile_button.event("on_click")
        def _(event):
            self.user_index = (self.user_index + 1) % len(self.user_profiles)
            user_profile_text.text = self.user_profiles[self.user_index].display_name
        self.ui.add(user_profile_button)

    def _start_game(self):
        game_view = SpaceShooterGameView(self)
        game_view.setup()
        self.window.show_view(game_view)

    def _start_ai_trainer(self):
        trainer_view = AITrainerView(self, self.user_profiles[self.user_index])
        self.window.show_view(trainer_view)

    def _quit_game(self):
        arcade.exit()


def load_fonts():
    arcade.resources.load_kenney_fonts()
    arcade.load_font("assets/fonts/Ithaca-LVB75.ttf")
    arcade.load_font("assets/fonts/PublicPixel-rv0pA.ttf")
    arcade.load_font("assets/fonts/Pixelzone-0v6y4.ttf")
    arcade.load_font("assets/fonts/PixeloidSans-E40en.ttf")


def main():
    load_fonts()
    window = arcade.Window(1280, 720, "TypeMania")
    main_menu_view = MainMenuView()
    window.show_view(main_menu_view)
    arcade.run()


if __name__ == "__main__":
    main()

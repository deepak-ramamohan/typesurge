import arcade
from space_shooter.views import SpaceShooterGameView
from ai_trainer.ai_trainer import AITrainerView
from utils.menu_view import MenuView


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

    def _start_game(self):
        game_view = SpaceShooterGameView(self)
        game_view.setup()
        self.window.show_view(game_view)

    def _start_ai_trainer(self):
        trainer_view = AITrainerView(self)
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

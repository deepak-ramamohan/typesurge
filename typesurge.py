import sys
import os
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS) # type: ignore

import arcade
from space_shooter.views import SSDifficultySelectionView
from typing_trainer.trainer_views import ModeSelectionView
from utils.menu_view import MenuView
from utils.resources import USER_PROFILE_SPRITE
from arcade.gui import (
    UIFlatButton, UIImage, UIOnClickEvent, UIAnchorLayout
)
from utils.button_styles import transparent_button_style
from utils.user_profile import UserProfile
from utils.resources import MAIN_MENU_MUSIC
from utils.music_manager import MusicManager
from utils import global_state


class MainMenuView(MenuView):
    """
    The main menu view.
    """

    def __init__(self) -> None:
        """
        Initializer
        """
        title_text = "Welcome to TypeSurge!"
        super().__init__(
            title_text=title_text,
            subtitle_text=""
        )
        space_shooter_button = self.create_button(
            "Space Shooter",
            tooltip_text="Shoot meteors with your keyboard before they destroy your spacecraft"
        )
        @space_shooter_button.event("on_click")
        def _(event: UIOnClickEvent) -> None:
            """
            Start the space shooter game.
            """
            self._start_game()

        typing_trainer_button = self.create_button(
            "Typing Trainer",
            tooltip_text="Measure and improve your typing skills"
        )
        @typing_trainer_button.event("on_click")
        def _(event: UIOnClickEvent) -> None:
            """
            Start the Typing trainer.
            """
            self._start_typing_trainer()
 
        quit_button = self.create_button(
            "Quit",
            tooltip_text="Quit to Desktop"
        )
        @quit_button.event("on_click")
        def _(event: UIOnClickEvent) -> None:
            """
            Quit the game.
            """
            self._quit_game()

        self.initialize_buttons(
            [
                space_shooter_button,
                typing_trainer_button,
                quit_button
            ]
        )

        MusicManager.play_music(MAIN_MENU_MUSIC)

        self._initialize_user_profile()
        
    def _initialize_user_profile(self) -> None:
        """
        Initialize the user profile.
        """
        self.user_profiles = [
            UserProfile(name="user_1", display_name="User 1"),
            UserProfile(name="user_2", display_name="User 2"),
            UserProfile(name="user_3", display_name="User 3")
        ]
        self.user_index = 0
        global_state.current_user_profile = self.user_profiles[self.user_index]
        IMAGE_SIZE = 50
        user_profile_button = UIFlatButton(
            text=f"{global_state.current_user_profile.display_name}",
            height=IMAGE_SIZE + 50,
            width=100,
            style=transparent_button_style
        )
        user_profile_button.place_text(anchor_x="center", anchor_y="bottom")
        user_profile_button.add(
            child=UIImage(
                texture=USER_PROFILE_SPRITE,
                width=IMAGE_SIZE,
                height=IMAGE_SIZE
            ),
            anchor_x="center",
            anchor_y="top",
            align_y=-5
        )

        @user_profile_button.event("on_click")
        def _(event: UIOnClickEvent) -> None:
            """
            Cycle through the user profiles.
            """
            self.user_index = (self.user_index + 1) % len(self.user_profiles)
            global_state.current_user_profile = self.user_profiles[self.user_index]
            user_profile_button.text = f"{global_state.current_user_profile.display_name}"

        user_profile_anchor = UIAnchorLayout()
        user_profile_anchor.add(
            user_profile_button,
            anchor_x="center",
            anchor_y="bottom",
            align_y=5
        )
        self.ui.add(user_profile_anchor)

    def on_show_view(self) -> None:
        """
        Handle show view.
        """
        super().on_show_view()
        if not MusicManager.is_music_playing_same(MAIN_MENU_MUSIC):
            MusicManager.play_music(MAIN_MENU_MUSIC)

    def _start_game(self) -> None:
        """
        Start the space shooter game.
        """
        game_view = SSDifficultySelectionView(self, self)
        self.window.show_view(game_view)

    def _start_typing_trainer(self) -> None:
        """
        Start the Typing trainer.
        """
        trainer_view = ModeSelectionView(self, self)
        self.window.show_view(trainer_view)

    def _quit_game(self) -> None:
        """
        Quit the game.
        """
        arcade.exit()


def load_fonts() -> None:
    """
    Load the fonts.
    """
    arcade.resources.load_kenney_fonts()
    arcade.load_font("assets/fonts/Ithaca-LVB75.ttf")
    arcade.load_font("assets/fonts/PublicPixel-rv0pA.ttf")
    arcade.load_font("assets/fonts/Pixelzone-0v6y4.ttf")
    arcade.load_font("assets/fonts/PixeloidSans-E40en.ttf")


def main() -> None:
    """
    Main function
    """
    load_fonts()
    window = arcade.Window(1280, 720, "TypeSurge")
    main_menu_view = MainMenuView()
    window.show_view(main_menu_view)
    arcade.run()


if __name__ == "__main__":
    main()

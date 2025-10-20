import arcade
from arcade.gui import (
    UIManager,
    UIAnchorLayout,
    UIBoxLayout, 
    UIFlatButton
)
from pyglet.graphics import Batch
from space_shooter.views import SpaceShooterGameView
from ai_trainer.ai_trainer import AITrainerView
from utils.colors import BROWN
from utils.button_styles import sepia_button_style
from utils.textures import SEPIA_BACKGROUND


class MainMenuView(arcade.View):

    def __init__(self):
        super().__init__()
        self.text_batch = Batch()
        self.title_text = arcade.Text(
            "Welcome to AI Typing Trainer!",
            x = self.window.width // 2,
            y = self.window.height // 2 + 50,
            anchor_x="center",
            font_name="Pixelzone",
            font_size=72,
            batch=self.text_batch,
            bold=True,
            color=BROWN
        )
        self.ui = UIManager()
        self.anchor = self.ui.add(UIAnchorLayout())
        self.BUTTON_WIDTH = 300
        self.space_shooter_button = UIFlatButton(
            text="Space Shooter",
            width=self.BUTTON_WIDTH,
            style=sepia_button_style
        )
        @self.space_shooter_button.event("on_click")
        def _(event):
            self._start_game()

        self.ai_trainer_button = UIFlatButton(
            text="AI Trainer", 
            width=self.BUTTON_WIDTH,
            style=sepia_button_style
        )
        @self.ai_trainer_button.event("on_click")
        def _(event):
            self._start_ai_trainer()
 
        self.quit_button = UIFlatButton(
            text="Quit",
            width=self.BUTTON_WIDTH,
            style=sepia_button_style
        )
        @self.quit_button.event("on_click")
        def _(event):
            self._quit_game()

        self.box_layout = UIBoxLayout(space_between=10)
        self.box_layout.add(self.space_shooter_button)
        self.box_layout.add(self.ai_trainer_button)
        self.box_layout.add(self.quit_button)
        
        self.anchor.add(
            self.box_layout, 
            anchor_y="top", 
            align_y=-(self.height - self.title_text.y + 60)
        )

    def on_show_view(self):
        # self.window.default_camera.use()
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_draw(self):
        self.clear() # This is IMPORTANT! The text looks jagged without this!
        arcade.draw_texture_rect(
            SEPIA_BACKGROUND,
            arcade.LBWH(0, 0, self.window.width, self.window.height)
        )
        self.text_batch.draw()
        self.ui.draw()

    def _start_game(self):
        game_view = SpaceShooterGameView(self)
        game_view.setup()
        self.window.show_view(game_view)

    def _start_ai_trainer(self):
        trainer_view = AITrainerView(self)
        trainer_view.setup()
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
    window = arcade.Window(1280, 720, "AI Typing Trainer")
    main_menu_view = MainMenuView()
    window.show_view(main_menu_view)
    arcade.run()


if __name__ == "__main__":
    main()

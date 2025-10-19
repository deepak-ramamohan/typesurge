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


class MainMenuView(arcade.View):

    BACKGROUND_COLOR = arcade.color.BLACK

    def __init__(self):
        super().__init__(background_color=self.BACKGROUND_COLOR)
        self.text_batch = Batch()
        self.title_text = arcade.Text(
            "Welcome to AI Typing Trainer!",
            x = self.window.width // 2,
            y = self.window.height // 2 + 50,
            anchor_x="center",
            font_size=40,
            batch=self.text_batch
        )
        self.instruction_text = arcade.Text(
            "Press ENTER to start or ESCAPE to quit", 
            x = self.title_text.x,
            y = self.title_text.y - 50,
            anchor_x="center",
            font_size=20,
            batch=self.text_batch
        )
        self.ui = UIManager()
        self.anchor = self.ui.add(UIAnchorLayout())
        self.BUTTON_WIDTH = 200
        
        self.space_shooter_button = UIFlatButton(width=self.BUTTON_WIDTH, text="Space Shooter")
        @self.space_shooter_button.event("on_click")
        def _(event):
            self._start_game()

        self.ai_trainer_button = UIFlatButton(width=self.BUTTON_WIDTH, text="AI Trainer")
        @self.ai_trainer_button.event("on_click")
        def _(event):
            self._start_ai_trainer()
 
        self.quit_button = UIFlatButton(width=self.BUTTON_WIDTH, text="Quit")
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
            align_y=-(self.height - self.title_text.y + 80)
        )

    def on_show_view(self):
        self.window.default_camera.use()
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_draw(self):
        self.clear() # This is IMPORTANT! The text looks jagged without this!
        self.text_batch.draw()
        self.ui.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            self._start_game()
        elif symbol == arcade.key.ESCAPE:
            self._quit_game()

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


def main():
    arcade.resources.load_kenney_fonts()
    window = arcade.Window(1280, 720, "AI Typing Trainer")
    main_menu_view = MainMenuView()
    window.show_view(main_menu_view)
    arcade.run()


if __name__ == "__main__":
    main()

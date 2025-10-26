import arcade
from arcade.gui import (
    UIManager,
    UIAnchorLayout,
    UIBoxLayout, 
    UIFlatButton
)
from pyglet.graphics import Batch
from utils.colors import BROWN
from utils.button_styles import sepia_button_style
from utils.resources import SEPIA_BACKGROUND


class MenuView(arcade.View):
    """
    Common class for creating consistent menu screens in the game
    """

    FONT_NAME = "Pixelzone"
    TITLE_FONT_SIZE = 72
    TITLE_OFFSET_FROM_CENTER = 50
    SUBTITLE_FONT_SIZE = 48
    SUBTITLE_OFFSET_FROM_TITLE = -70
    BUTTON_WIDTH = 300
    BUTTON_OFFSET_FROM_SUBTITLE = -30

    def __init__(
        self,
        title_text: str,
        subtitle_text: str
    ) -> None:
        super().__init__()
        self.text_batch = Batch()
        self.title_text = arcade.Text(
            title_text,
            x = self.window.width // 2,
            y = self.window.height // 2 + self.TITLE_OFFSET_FROM_CENTER,
            anchor_x="center",
            font_name=self.FONT_NAME,
            font_size=self.TITLE_FONT_SIZE,
            batch=self.text_batch,
            bold=True,
            color=BROWN
        )
        self.subtitle_text = arcade.Text(
            subtitle_text,
            x = self.title_text.x,
            y = self.title_text.y + self.SUBTITLE_OFFSET_FROM_TITLE,
            anchor_x="center",
            font_name=self.FONT_NAME,
            font_size=self.SUBTITLE_FONT_SIZE,
            color=BROWN,
            batch=self.text_batch
        )
        self.ui = UIManager()
        self.anchor = self.ui.add(UIAnchorLayout())
        self.box_layout = UIBoxLayout(space_between=15)
        self.current_music = None

    def on_draw(self):
        """
        Performs the following operations:
        1. Clears the screen
        2. Draws the theme background
        3. Draws the title and subtitle text elements
        4. Draws the UI buttons
        """
        self.clear() # This is IMPORTANT! The text looks jagged without this!
        arcade.draw_texture_rect(
            SEPIA_BACKGROUND,
            arcade.LBWH(0, 0, self.window.width, self.window.height)
        )
        self.text_batch.draw()
        self.ui.draw()

    def on_show_view(self):
        self.ui.enable()
        if self.current_music:
            self.current_music.play()

    def on_hide_view(self):
        self.ui.disable()
        if self.current_music:
            self.current_music.pause()

    @classmethod
    def create_button(cls, button_text):
        """
        Creates a standardized button
        """
        button = UIFlatButton(
            text=button_text,
            width=cls.BUTTON_WIDTH,
            style=sepia_button_style
        )
        return button
    
    def initialize_buttons(self, buttons_list):
        """
        Create all the buttons from the list
        """
        for button in buttons_list:
            self.box_layout.add(button)
        self.anchor.add(
            self.box_layout, 
            anchor_y="top", 
            align_y=-(self.height - self.subtitle_text.y - self.BUTTON_OFFSET_FROM_SUBTITLE)
        )
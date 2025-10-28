from arcade.gui import UIFlatButton
from utils.colors import BROWN, BEIGE, TRANSPARENT


BUTTON_FONT_NAME = "Pixelzone"
SEPIA_BUTTON_FONT_SIZE = 30
sepia_button_style = {
    "normal": UIFlatButton.UIStyle(
        font_name=BUTTON_FONT_NAME,
        font_size=SEPIA_BUTTON_FONT_SIZE,
        font_color=BEIGE,
        bg=BROWN
    ),
    "hover": UIFlatButton.UIStyle(
        font_name=BUTTON_FONT_NAME,
        font_size=SEPIA_BUTTON_FONT_SIZE,
        font_color=BEIGE,
        bg=BROWN,
        border=BEIGE,
        border_width=2
    ),
    "press": UIFlatButton.UIStyle(
        font_name=BUTTON_FONT_NAME,
        font_size=SEPIA_BUTTON_FONT_SIZE,
        font_color=BEIGE,
        bg=BROWN,
        border=BEIGE,
        border_width=4
    )
}


TRANSPARENT_BUTTON_FONT_SIZE = 28
transparent_button_style = {
    "normal": UIFlatButton.UIStyle(
        font_name=BUTTON_FONT_NAME,
        font_size=TRANSPARENT_BUTTON_FONT_SIZE,
        font_color=BROWN,
        bg=TRANSPARENT
    ),
    "hover": UIFlatButton.UIStyle(
        font_name=BUTTON_FONT_NAME,
        font_size=TRANSPARENT_BUTTON_FONT_SIZE,
        font_color=BROWN,
        bg=TRANSPARENT,
        border=BROWN,
        border_width=1
    ),
    "press": UIFlatButton.UIStyle(
        font_name=BUTTON_FONT_NAME,
        font_size=TRANSPARENT_BUTTON_FONT_SIZE,
        font_color=BROWN,
        bg=TRANSPARENT,
        border=BROWN,
        border_width=2
    )
}
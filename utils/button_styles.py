from arcade.gui import UIFlatButton
from utils.colors import BROWN, BEIGE


BUTTON_FONT_NAME = "Pixelzone"
BUTTON_FONT_SIZE = 30
sepia_button_style = {
    "normal": UIFlatButton.UIStyle(
        font_name=BUTTON_FONT_NAME,
        font_size=BUTTON_FONT_SIZE,
        font_color=BEIGE,
        bg=BROWN
    ),
    "hover": UIFlatButton.UIStyle(
        font_name=BUTTON_FONT_NAME,
        font_size=BUTTON_FONT_SIZE,
        font_color=BEIGE,
        bg=BROWN,
        border=BEIGE,
        border_width=2
    ),
    "press": UIFlatButton.UIStyle(
        font_name=BUTTON_FONT_NAME,
        font_size=BUTTON_FONT_SIZE,
        font_color=BEIGE,
        bg=BROWN,
        border=BEIGE,
        border_width=4
    )
}
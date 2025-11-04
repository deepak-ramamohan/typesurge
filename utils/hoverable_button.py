import arcade
from arcade.gui import UIFlatButton

class HoverableButton(UIFlatButton):
    """
    A UIFlatButton that can store text to be displayed on hover.
    """
    def __init__(self, *args, hover_text: str = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.hover_text = hover_text

from arcade.gui import UIFlatButton


class UITooltipButton(UIFlatButton):
    """
    A UIFlatButton that can store tooltip text (e.g., to be displayed on hover).
    """
    def __init__(self, *args, tooltip_text: str = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.tooltip_text = tooltip_text

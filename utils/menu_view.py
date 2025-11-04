import arcade
from arcade.gui import (
    UIManager,
    UIAnchorLayout,
    UIBoxLayout,
    UIFlatButton,
    UILabel,
    UITextArea
)

from utils.colors import BROWN
from utils.button_styles import sepia_button_style
from utils.resources import SEPIA_BACKGROUND
from utils.hoverable_button import HoverableButton


class MenuView(arcade.View):
    """
    Common class for creating consistent menu screens in the game.
    Supports two layouts: a centered layout and a split layout with a canvas.
    """

    FONT_NAME = "Pixelzone"
    TITLE_FONT_SIZE = 72
    SUBTITLE_FONT_SIZE = 48
    BUTTON_WIDTH = 300

    def __init__(
        self,
        title_text: str,
        subtitle_text: str,
        previous_view: arcade.View | None = None,
        canvas: bool = False,
        canvas_ratio: float = 0.4
    ) -> None:
        super().__init__()
        self.has_canvas = canvas
        self.previous_view = previous_view

        # UI Manager and main layout
        self.ui = UIManager()
        self.anchor = self.ui.add(UIAnchorLayout(size_hint=(1, 1)))

        # Create title and subtitle labels
        self.title_label = UILabel(
            text=title_text,
            font_name=self.FONT_NAME,
            font_size=self.TITLE_FONT_SIZE,
            text_color=BROWN,
            bold=True,
            align="center",
            size_hint=(1, None) # Take full width of parent
        )
        self.subtitle_label = UILabel(
            text=subtitle_text,
            font_name=self.FONT_NAME,
            font_size=self.SUBTITLE_FONT_SIZE,
            text_color=BROWN,
            align="center",
            size_hint=(1, None) # Take full width of parent
        )

        if self.has_canvas:
            # Create a split layout
            # Left side for buttons and text
            left_pane = UIBoxLayout(
                size_hint=(canvas_ratio, 1),
                space_between=15,
                align="center"
            )
            self.anchor.add(left_pane, anchor_x="left", anchor_y="center_y")

            # Right side for canvas
            canvas_pane = UIAnchorLayout(size_hint=(1 - canvas_ratio, 1))
            self.anchor.add(canvas_pane, anchor_x="right", anchor_y="center_y")

            # The hover text display area in the canvas
            self.hover_text_area = UITextArea(
                text="",
                text_color=BROWN,
                font_name=self.FONT_NAME,
                font_size=24,
                multiline=True,
                size_hint=(0.9, 0.9)
            )
            canvas_pane.add(self.hover_text_area, anchor_x="center_x", anchor_y="center_y")

            self.button_box = left_pane # Buttons will be added here
            self.button_box.add(self.title_label)
            self.button_box.add(self.subtitle_label)

        else:
            # Create a centered layout
            center_pane = UIBoxLayout(space_between=15, align="center")
            self.anchor.add(center_pane, anchor_x="center_x", anchor_y="center_y")

            self.button_box = center_pane # Buttons will be added here
            self.button_box.add(self.title_label)
            self.button_box.add(self.subtitle_label)

    def on_draw(self) -> None:
        """
        Performs the following operations:
        1. Clears the screen
        2. Draws the theme background
        3. Draws the UI
        """
        self.clear()
        arcade.draw_texture_rect(
            SEPIA_BACKGROUND,
            arcade.LBWH(0, 0, self.window.width, self.window.height)
        )
        self.ui.draw()

    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    def return_to_previous_view(self) -> None:
        if self.previous_view is not None:
            self.window.show_view(self.previous_view)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.return_to_previous_view()

    @classmethod
    def create_button(cls, button_text: str, hover_text: str = "") -> HoverableButton:
        """
        Creates a standardized button.
        """
        button = HoverableButton(
            text=button_text,
            width=cls.BUTTON_WIDTH,
            style=sepia_button_style,
            hover_text=hover_text
        )
        return button

    def initialize_buttons(self, buttons_list: list[UIFlatButton]) -> None:
        """
        Adds buttons to the layout and sets up hover events if needed.
        """
        for button in buttons_list:
            self.button_box.add(button)
            if self.has_canvas and isinstance(button, HoverableButton):
                # Using a closure to capture the correct button instance
                def make_hover_handler(btn):
                    def on_hover(event):
                        self.hover_text_area.text = btn.hover_text
                    return on_hover

                def make_unhover_handler():
                    def on_unhover(event):
                        self.hover_text_area.text = ""
                    return on_unhover

                button.event("on_hover")(make_hover_handler(button))
                button.event("on_unhover")(make_unhover_handler())

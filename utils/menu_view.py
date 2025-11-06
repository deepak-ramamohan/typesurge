import arcade
from arcade.gui import (
    UIManager,
    UIAnchorLayout,
    UIBoxLayout,
    UILabel,
    UISpace
)
from utils.colors import BROWN
from utils.button_styles import sepia_button_style
from utils.resources import SEPIA_BACKGROUND
from utils.ui_tooltip_button import UITooltipButton


class MenuView(arcade.View):
    """
    Common class for creating consistent menu screens in the game.
    """

    FONT_NAME = "Pixelzone"
    TITLE_FONT_SIZE = 72
    SUBTITLE_FONT_SIZE = 48
    BUTTON_WIDTH = 300
    PADDING = 20

    def __init__(
        self,
        title_text: str,
        subtitle_text: str,
        previous_view: arcade.View | None = None
    ) -> None:
        super().__init__()
        self.previous_view = previous_view

        # UI Manager and main layout
        self.ui = UIManager()
        self.root_box_layout = self.ui.add(UIBoxLayout(vertical=True, size_hint=(1, 1), space_between=self.PADDING))
        # Create title and subtitle labels
        self.title_label = UILabel(
            text=title_text,
            font_name=self.FONT_NAME,
            font_size=self.TITLE_FONT_SIZE,
            text_color=BROWN,
            bold=True,
            align="center",
            size_hint=(1, 1) # Take full width of parent
        )
        self.subtitle_label = UILabel(
            text=subtitle_text,
            font_name=self.FONT_NAME,
            font_size=self.SUBTITLE_FONT_SIZE,
            text_color=BROWN,
            align="center",
            size_hint=(1, 1) # Take full width of parent
        )
        self.header_box = UIBoxLayout(vertical=True)
        self.header_box.add(UISpace(height=self.PADDING))
        self.header_box.add(self.title_label)
        self.header_box.add(self.subtitle_label)
        self.header_box.add(UISpace(height=self.PADDING))
        
        # Create an anchor for the root. This will help center the layout
        self.root_anchor = self.root_box_layout.add(UIAnchorLayout())
        # The content box will contain the headers and the button pane
        self.content_box = self.root_anchor.add(
            UIBoxLayout(
                vertical=True, 
                space_between=self.PADDING
            ),
            anchor_x="center",
            anchor_y="center"
        )
        # Add the header box (title and subtitle labels) to the content box
        self.content_box.add(self.header_box)
        self.button_pane = self.content_box.add(
            UIBoxLayout(vertical=True, space_between=self.PADDING),
            anchor_y="center"
        )
        self.content_box.add(UISpace(height=0))
        self.tooltip_space = UISpace(height=50)
        self.content_box.add(self.tooltip_space)
        self.tooltip_text = UILabel(
            text=" ",
            width=self.window.width - 100,
            height=100,
            font_size=32,
            font_name=self.FONT_NAME,
            text_color=BROWN,
            align="center",
            multiline=False
        )
        self.is_tooltip_added = False

        self.buttons_list = []

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
        if not self.is_tooltip_added:
            self._add_tooltip_to_layout()
        self._update_tooltip_text()

    def on_show_view(self) -> None:
        # self._reset_hover()
        self.ui.enable()

    def on_hide_view(self) -> None:
        self._reset_hover()
        self.ui.disable()

    def return_to_previous_view(self) -> None:
        if self.previous_view is not None:
            self.window.show_view(self.previous_view)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.return_to_previous_view()

    @classmethod
    def create_button(cls, button_text: str, tooltip_text: str = "") -> UITooltipButton:
        """
        Creates a standardized button.
        """
        button = UITooltipButton(
            text=button_text,
            width=cls.BUTTON_WIDTH,
            style=sepia_button_style,
            tooltip_text=tooltip_text
        )
        return button

    def initialize_buttons(self, buttons_list: list[UITooltipButton]) -> None:
        """
        Adds buttons to the layout and sets up hover events if needed.
        """
        self.buttons_list = buttons_list
        for button in buttons_list:
            self.button_pane.add(button)

    def _add_tooltip_to_layout(self):
        self.root_anchor.add(
            self.tooltip_text,
            anchor_x="center",
            anchor_y="bottom",
            align_y=self.tooltip_space.center_y
        )
        self.is_tooltip_added = True

    def _update_tooltip_text(self):
        self.tooltip_text.text = ""
        for button in self.buttons_list:
            if button.hovered:
                self.tooltip_text.text = button.tooltip_text

    def _reset_hover(self):
        for button in self.buttons_list:
            button.hovered = False
        self._update_tooltip_text()

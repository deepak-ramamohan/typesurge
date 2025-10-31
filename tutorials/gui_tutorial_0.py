import arcade
from arcade.gui import (
    UIManager,
    UITextureButton,
    UIAnchorLayout,
    UIView
)

# Pre-loading textures
TEX_RED_BUTTON_NORMAL = arcade.load_texture(":resources:gui_basic_assets/button/red_normal.png")
TEX_RED_BUTTON_HOVER = arcade.load_texture(":resources:gui_basic_assets/button/red_hover.png")
TEX_RED_BUTTON_PRESS = arcade.load_texture(":resources:gui_basic_assets/button/red_press.png")


class GreenView(arcade.View):
    """
    A view with a green background.
    """

    def __init__(self, window: arcade.Window | None = None, background_color: tuple[int, int, int] | None = None) -> None:
        """
        Initializer
        """
        super().__init__(window)

        self.ui = UIManager()
        self.background_color = arcade.uicolor.GREEN_EMERALD
        anchor = self.ui.add(UIAnchorLayout())

        button = anchor.add(
            UITextureButton(
                text="Switch to BLUE view",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_hovered=TEX_RED_BUTTON_HOVER,
                texture_pressed=TEX_RED_BUTTON_PRESS
            )
        )

        @button.event
        def on_click(event: "UIOnClickEvent") -> None:
            """
            Switch to the blue view.
            """
            self.window.show_view(BlueView())
    
    def on_show_view(self) -> None:
        """
        This is run once when we switch to this view
        """
        self.ui.enable()
    
    def on_hide_view(self) -> None:
        """
        This is run once when we switch away from this view
        """
        self.ui.disable()

    def on_draw(self) -> None:
        """
        Draw this view
        """
        self.clear()

        self.ui.draw()


class BlueView(UIView):
    """
    A view with a blue background.
    """

    def __init__(self) -> None:
        """
        Initializer
        """
        super().__init__()
        self.background_color = arcade.uicolor.BLUE_PETER_RIVER

        anchor = self.add_widget(UIAnchorLayout())

        button = anchor.add(
            UITextureButton(
                text="Switch to GREEN view",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_hovered=TEX_RED_BUTTON_HOVER,
                texture_pressed=TEX_RED_BUTTON_PRESS
            )
        )

        @button.event
        def on_click(event: "UIOnClickEvent") -> None:
            """
            Switch to the green view.
            """
            self.window.show_view(GreenView())


def main() -> None:
    """
    Main function
    """
    window = arcade.Window(title="GUI Example: Basic Setup")
    window.show_view(GreenView())
    arcade.run()


if __name__ == "__main__":
    main()
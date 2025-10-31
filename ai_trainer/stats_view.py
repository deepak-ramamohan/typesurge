import arcade
import matplotlib.pyplot as plt
from arcade.gui import UIOnClickEvent
import numpy as np
from utils.menu_view import MenuView
import io
from PIL import Image
from utils.save_manager import SaveManager
from utils import global_state
from utils.colors import BROWN, BROWN_DARK

class StatsView(MenuView):
    """
    The stats view.
    """

    def __init__(self, previous_view: arcade.View) -> None:
        """
        Initializer
        """
        super().__init__(
            title_text="Session Stats",
            subtitle_text="",
            previous_view=previous_view
        )
        self.save_manager = SaveManager(global_state.current_user_profile)
        self.session_stats = self.save_manager.get_all_session_stats()
        self.plot_texture = None

        if not self.session_stats:
            self.subtitle_text.text = "No stats available yet. Play a session to see your progress!"
        else:
            self._generate_plot()

        back_button = self.create_button("Back")
        @back_button.event("on_click")
        def _(event: "UIOnClickEvent") -> None:
            """
            Return to the previous view.
            """
            self.return_to_previous_view()

        self.initialize_buttons([back_button])

    def _generate_plot(self) -> None:
        """
        Generate the plot and load it into a texture.
        """
        wpm_data = [stat.wpm for stat in self.session_stats]
        accuracy_data = [stat.accuracy * 100 for stat in self.session_stats]
        sessions = [f"Session {i+1}" for i in range(len(self.session_stats))]

        fig, ax1 = plt.subplots()

        # Bar plot for WPM
        ax1.bar(sessions, wpm_data, color=[(c/255) for c in BROWN], label='WPM')
        ax1.set_xlabel('Session')
        ax1.set_ylabel('Words Per Minute (WPM)', color=[(c/255) for c in BROWN])
        ax1.tick_params(axis='y', labelcolor=[(c/255) for c in BROWN])

        # Line plot for Accuracy
        ax2 = ax1.twinx()
        ax2.plot(sessions, accuracy_data, color=[(c/255) for c in BROWN_DARK], label='Accuracy (%)')
        ax2.set_ylabel('Accuracy (%)', color=[(c/255) for c in BROWN_DARK])
        ax2.tick_params(axis='y', labelcolor=[(c/255) for c in BROWN_DARK])
        ax2.set_ylim(0, 100)

        fig.tight_layout()
        fig.patch.set_alpha(0.0)
        ax1.patch.set_alpha(0.0)
        ax2.patch.set_alpha(0.0)

        # Save plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)
        buf.seek(0)

        # Create an arcade texture from the buffer
        image = Image.open(buf)
        self.plot_texture = arcade.Texture(image)

        plt.close(fig)

    def on_draw(self) -> None:
        """
        Draw the view.
        """
        super().on_draw()
        if self.plot_texture:
            self.plot_texture.draw_sized(
                center_x=self.window.width / 2,
                center_y=self.window.height / 2,
                width=self.window.width - 200,
                height=self.window.height - 400
            )

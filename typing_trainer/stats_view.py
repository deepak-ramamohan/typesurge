import arcade
import io
import matplotlib.pyplot as plt
from arcade.gui import UIOnClickEvent, UISpace
import matplotlib.font_manager as fm
from utils.menu_view import MenuView
from PIL import Image
from utils.save_manager import SaveManager
from utils import global_state
from utils.colors import BROWN

class StatsView(MenuView):
    """
    The stats view.
    """

    def __init__(self, previous_view: arcade.View) -> None:
        """
        Initializer
        """
        title_text = "Session Stats"
        subtitle_text = ""
        self.save_manager = SaveManager(global_state.current_user_profile)
        self.session_stats = self.save_manager.get_all_session_stats(limit=20)
        self.total_session_count = self.save_manager.get_number_of_sessions()
        self.plot_texture = None

        if not self.session_stats:
            subtitle_text = "No stats available yet. Play a session to see your progress!"
        
        super().__init__(
            title_text=title_text,
            subtitle_text=subtitle_text,
            previous_view=previous_view
        )

        back_button = self.create_button("Back")
        @back_button.event("on_click")
        def _(event: UIOnClickEvent) -> None:
            """
            Return to the previous view.
            """
            self.return_to_previous_view()

        if self.session_stats:
            self.drawing_space = UISpace(height=int(self.window.height * 0.65))
            self.header_box.add(self.drawing_space)
            self._generate_plot()

        self.initialize_buttons([back_button])

    def _generate_plot(self) -> None:
        """
        Generate the plot and load it into a texture.
        """
        wpm_data = [stat.wpm for stat in self.session_stats]
        accuracy_data = [stat.accuracy * 100 for stat in self.session_stats]
        num_sessions = len(self.session_stats)
        sessions = [
            str(i) for i in range(
                self.total_session_count - num_sessions + 1, 
                self.total_session_count + 1
            )
        ]

        # Add Pixelzone font
        font_path = 'assets/fonts/Pixelzone-0v6y4.ttf'
        fm.fontManager.addfont(font_path)
        plt.rcParams['font.family'] = 'Pixelzone'

        LABEL_FONT_SIZE = 42

        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(20, 8))

        # Line plot for WPM
        ax1.plot(sessions, wpm_data, color=[(c/255) for c in BROWN], label='WPM', marker='*')
        ax1.set_ylabel('Words Per Minute (WPM)', color=[(c/255) for c in BROWN], fontsize=LABEL_FONT_SIZE, fontweight='bold')
        ax1.tick_params(axis='y', labelcolor=[(c/255) for c in BROWN], labelsize=LABEL_FONT_SIZE)
        ax1.tick_params(axis='x', labelcolor=[(c/255) for c in BROWN], labelsize=LABEL_FONT_SIZE)
        ax1.set_ylim(0, max(wpm_data) + 10)

        label_offset = (max(wpm_data) + 10) / 40
        for i, txt in enumerate(wpm_data):
            ax1.text(sessions[i], wpm_data[i] - label_offset, f'{txt:.0f}', va='top', ha='center', fontsize=LABEL_FONT_SIZE, color=[(c/255) for c in BROWN], fontweight='bold')

        # Line plot for Accuracy
        def transform(y):
            if y >= 90:
                return 0.4 + (y - 90) / 10 * 0.6
            elif y >= 80:
                return 0.2 + (y - 80) / 10 * 0.2
            else:
                return y / 80 * 0.2

        transformed_accuracy_data = [transform(y) for y in accuracy_data]
        ax2.plot(sessions, transformed_accuracy_data, color=[(c/255) for c in BROWN], label='Accuracy (%)', marker='*')
        ax2.set_xlabel('Session', fontsize=LABEL_FONT_SIZE, fontweight='bold', color=[(c/255) for c in BROWN])
        ax2.set_ylabel('Accuracy (%)', color=[(c/255) for c in BROWN], fontsize=LABEL_FONT_SIZE, fontweight='bold')
        ax2.tick_params(axis='y', labelcolor=[(c/255) for c in BROWN], labelsize=LABEL_FONT_SIZE)
        ax2.tick_params(axis='x', labelcolor=[(c/255) for c in BROWN], labelsize=LABEL_FONT_SIZE)
        ax2.set_ylim(0, 1)

        # Set custom y-axis ticks and labels
        tick_positions = [transform(y) for y in [0, 80, 90, 100]]
        tick_labels = ['0%', '80%', '90%', '100%']
        ax2.set_yticks(tick_positions)
        ax2.set_yticklabels(tick_labels)

        for i, txt in enumerate(accuracy_data):
            ax2.text(
                sessions[i], 
                transformed_accuracy_data[i] - 0.04, 
                f'{txt:.1f}%', 
                va='top', 
                ha='center', 
                fontsize=LABEL_FONT_SIZE, 
                color=[(c/255) for c in BROWN], 
                fontweight='bold'
            )
        
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
            plot_aspect_ratio = self.plot_texture.width / self.plot_texture.height
            plot_width = self.window.width - 100
            plot_height = plot_width / plot_aspect_ratio

            # height_cap = self.window.height - 250
            height_cap = self.drawing_space.rect.height

            # Ensure the plot doesn't exceed the screen height
            if plot_height > height_cap:
                plot_height = height_cap
                plot_width = plot_height * plot_aspect_ratio

            arcade.draw_texture_rect(
                texture=self.plot_texture,
                rect=arcade.XYWH(
                    x=self.window.width / 2,
                    y=self.window.height / 2,
                    width=plot_width,
                    height=plot_height
                )
            )

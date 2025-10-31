import arcade
from arcade.gui import UIOnClickEvent
import pyglet
from pyglet.graphics import Batch
from pyglet.text import caret
from utils.word_manager import WordManager
from utils.resources import SEPIA_BACKGROUND
from utils.colors import BROWN
from utils.menu_view import MenuView
from utils.save_manager import SaveManager
from utils import global_state
from utils.resources import AI_TRAINER_MUSIC
from utils.music_manager import MusicManager
from ai_trainer.session_stats import SessionStats
from ai_trainer.stats_view import StatsView


class AITrainerView(arcade.View):
    """
    The AI Trainer view.
    """

    UNMATCHED_TEXT_COLOR = BROWN[:3] + (170,)
    CORRECT_TEXT_COLOR = BROWN
    INCORRECT_TEXT_COLOR = arcade.color.AUBURN
    WPM_TEXT_COLOR = arcade.color.ANTIQUE_RUBY
    FONT_NAME = "Pixelzone"
    WORD_CHARACTER_COUNT_MIN = 4
    WORD_CHARACTER_COUNT_MAX = 8
    SPACE_CHAR = '·'

    def __init__(self, main_menu_view: arcade.View, words_count: int) -> None:
        """
        Initializer
        """
        super().__init__()
        self.background = SEPIA_BACKGROUND
        self.main_menu_view = main_menu_view
        self.words_count = words_count
        save_manager = SaveManager(global_state.current_user_profile) 
        self.word_manager = WordManager()
        # self.words_list = [
        #     self.word_manager.generate_word(
        #         min_character_count=self.WORD_CHARACTER_COUNT_MIN,
        #         max_character_count=self.WORD_CHARACTER_COUNT_MAX
        #     )
        #     for _ in range(self.words_count)
        # ]
        self.words_list = self.word_manager.get_weighted_sample(
            num_words=self.words_count,
            char_accuracies=save_manager.get_char_accuracies(),
            word_mistype_counts=save_manager.get_word_mistype_counts(),
            min_character_count=self.WORD_CHARACTER_COUNT_MIN,
            max_character_count=self.WORD_CHARACTER_COUNT_MAX
        )
        self.word_index = 0
        self.input_text = " ".join(self.words_list)
        self.padding_size = 150
        self.padded_text = " " * self.padding_size + self.input_text + " " * self.padding_size
        self.session_stats = SessionStats()
        self.pyglet_batch = Batch()
        self.text_document = pyglet.text.document.FormattedDocument(
            text=self.padded_text
        )
        self.text_document.set_style(
            start=0, 
            end=len(self.text_document.text),
            attributes=dict(
                font_name=self.FONT_NAME,
                font_size=68,
                color=self.UNMATCHED_TEXT_COLOR
            )
        )
        self.text_layout = pyglet.text.layout.IncrementalTextLayout(
            document=self.text_document,
            width=int(self.width - 50),
            height=100,
            x=self.width//2,
            y=self.height//2 + 50,
            anchor_x="center",
            anchor_y="center",
            multiline=False,
            batch=self.pyglet_batch
        )
        self.caret = caret.Caret(
            self.text_layout,
            color=BROWN
        )
        self.caret.position = self.padding_size
        self.center_text_layout()
        self.wpm_text = arcade.Text(
            "",
            x=self.window.width//2,
            y=20,
            anchor_x="center",
            font_name="Pixelzone",
            font_size=50,
            color=self.WPM_TEXT_COLOR,
            batch=self.pyglet_batch
        )
        self.typing_sound = arcade.Sound("assets/sounds/eklee-KeyPressMac06.wav")
        MusicManager.play_music(AI_TRAINER_MUSIC) 
    
    def on_draw(self) -> None:
        """
        Draw the view.
        """
        self.clear()
        arcade.draw_texture_rect(
            SEPIA_BACKGROUND,
            arcade.LBWH(0, 0, self.window.width, self.window.height)
        )
        self.pyglet_batch.draw()

    def capture_character_input(self, input: str) -> None:
        """
        Capture the character input.
        """
        correct_char = self.padded_text[self.caret.position]
        self.session_stats.char_confusion_matrix[correct_char][input] += 1
        if input == correct_char:
            self.session_stats.chars_typed_correctly += 1
            self.text_document.set_style(
                self.caret.position,
                self.caret.position + 1,
                attributes=dict(
                    color=self.CORRECT_TEXT_COLOR
                )
            )
        else:
            self.text_document.delete_text(self.caret.position, self.caret.position + 1)
            if input == " ":
                self.text_document.insert_text(self.caret.position, self.SPACE_CHAR)
            else:
                self.text_document.insert_text(self.caret.position, input)
            self.text_document.set_style(
                self.caret.position,
                self.caret.position + 1,
                attributes=dict(
                    color=self.INCORRECT_TEXT_COLOR
                )
            )
            self.session_stats.word_mistype_counts[self.words_list[self.word_index]] += 1
        if correct_char == " ":
            self.word_index += 1
        self.session_stats.chars_typed_total += 1
        self.caret.position += 1
        if self.caret.position == self.padding_size + len(self.input_text):
            self._complete_game()
        self.center_text_layout()

    def capture_backspace(self) -> None:
        """
        Capture the backspace key.
        """
        if self.caret.position > self.padding_size:
            self.caret.position -= 1
            correct_char = self.padded_text[self.caret.position]
            self.text_document.delete_text(self.caret.position, self.caret.position + 1)
            self.text_document.insert_text(self.caret.position, correct_char)
            self.text_document.set_style(
                start=self.caret.position,
                end=self.caret.position + 1,
                attributes=dict(
                    color=self.UNMATCHED_TEXT_COLOR
                )
            )
            self.center_text_layout()
            if correct_char == " ":
                self.word_index -= 1

    def center_text_layout(self) -> None:
        """
        Updates the horizontal scroll on the layout so that the caret is in the center
        """    
        caret_x_pos = self.text_layout.get_point_from_position(self.caret.position)[0]
        self.text_layout.view_x = int(caret_x_pos - (self.window.width / 2))

    def on_update(self, delta_time: float) -> None:
        """
        Update the view.
        """
        self.session_stats.duration_seconds += delta_time
        if self.session_stats.duration_seconds >= 2:
            self.session_stats.wpm = (
                self.session_stats.chars_typed_correctly * 12 / self.session_stats.duration_seconds
            )
        if self.session_stats.chars_typed_total > 0:
            self.session_stats.accuracy = self.session_stats.chars_typed_correctly / self.session_stats.chars_typed_total
        self.wpm_text.text = f"WPM: {self.session_stats.wpm:.1f}, " + \
            f"Accuracy: {100.0 * self.session_stats.accuracy:.2f}%"
        
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """
        Handle key presses.
        """
        if symbol == arcade.key.ESCAPE:
            pause_view = PauseView(self, self.session_stats)
            self.window.show_view(pause_view)
        else:
            self._play_typing_sound()

    def _complete_game(self) -> None:
        """
        Complete the game.
        """
        game_completed_view = GameCompletedView(self, self.session_stats)
        self.window.show_view(game_completed_view)

    def _play_typing_sound(self) -> None:
        """
        Play the typing sound.
        """
        arcade.play_sound(self.typing_sound, volume=0.75)

    def on_text(self, text: str) -> None:
        """
        Captures unicode text input after applying modifiers.
        This works (even though it's not mentioned in arcade's documentation) 
        because arcade probably inherits pyglet.window
        """
        if text not in {'\r', '\n', '\r\n'}:
            self.capture_character_input(input=text)
            
    def on_text_motion(self, motion: int) -> None:
        """
        Identifying when the backspace key is pressed (or held pressed)
        """
        if motion == arcade.key.MOTION_BACKSPACE:
            self.capture_backspace()
    
    def on_show_view(self) -> None:
        """
        Handle show view.
        """
        self.window.set_mouse_visible(False)

    def on_hide_view(self) -> None:
        """
        Handle hide view.
        """
        self.window.set_mouse_visible(True)


class PauseView(MenuView):
    """
    The pause view.
    """

    def __init__(self, game_view: AITrainerView, session_stats: SessionStats) -> None:
        """
        Initializer
        """
        self.game_view = game_view
        self.save_manager = SaveManager(global_state.current_user_profile)
        self.session_stats = session_stats
        self.TITLE_OFFSET_FROM_CENTER = 100
        self.TITLE_FONT_SIZE = 64
        score_text = f"WPM: {self.session_stats.wpm:.1f}," + \
            f" Accuracy: {100.0 * self.session_stats.accuracy:.2f}%"
        super().__init__(
            title_text="Game Paused",
            subtitle_text=score_text
        )

        resume_button = self.create_button("Resume")
        @resume_button.event("on_click")
        def _(event: "UIOnClickEvent") -> None:
            """
            Resume the game.
            """
            self._resume()

        quit_to_main_menu_button = self.create_button("Quit to Main Menu")
        @quit_to_main_menu_button.event("on_click")
        def _(event: "UIOnClickEvent") -> None:
            """
            Return to the main menu.
            """
            self._return_to_main_menu()

        self.initialize_buttons(
            [
                resume_button,
                quit_to_main_menu_button
            ]
        )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """
        Handle key presses.
        """
        if symbol == arcade.key.ESCAPE:
            self._resume()

    def _resume(self) -> None:
        """
        Resume the game.
        """
        self.window.show_view(self.game_view)

    def _return_to_main_menu(self) -> None:
        """
        Return to the main menu.
        """
        self.save_manager.save_session_stats_to_db(self.session_stats)
        # self.save_manager.load_and_print_db()
        self.window.show_view(self.game_view.main_menu_view)


class GameCompletedView(MenuView):
    """
    The game completed view.
    """

    def __init__(self, game_view: AITrainerView, session_stats: SessionStats) -> None:
        """
        Initializer
        """
        self.game_view = game_view
        self.save_manager = SaveManager(global_state.current_user_profile)
        self.session_stats = session_stats
        self.TITLE_OFFSET_FROM_CENTER = 100
        self.TITLE_FONT_SIZE = 64
        score_text = f"WPM: {self.session_stats.wpm:.1f}," + \
            f" Accuracy: {100.0 * self.session_stats.accuracy:.2f}%"
        super().__init__(
            title_text="Session Completed!",
            subtitle_text=score_text
        )

        continue_button = self.create_button("Continue")
        @continue_button.event("on_click")
        def _(event: "UIOnClickEvent") -> None:
            """
            Return to the main menu.
            """
            self._return_to_main_menu()

        self.initialize_buttons(
            [
                continue_button
            ]
        )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """
        Handle key presses.
        """
        if symbol == arcade.key.ESCAPE:
            self._return_to_main_menu()

    def _return_to_main_menu(self) -> None:
        """
        Return to the main menu.
        """
        self.save_manager.save_session_stats_to_db(self.session_stats)
        # self.save_manager.load_and_print_db()
        self.window.show_view(self.game_view.main_menu_view)


class ModeSelectionView(MenuView):
    """
    The mode selection view.
    """

    def __init__(self, previous_view: arcade.View, main_menu_view: arcade.View) -> None:
        """
        Initializer
        """
        self.main_menu_view = main_menu_view
        self.user_profile = global_state.current_user_profile
        self.TITLE_OFFSET_FROM_CENTER = 100
        self.TITLE_FONT_SIZE = 64
        super().__init__(
            title_text="AI Trainer",
            subtitle_text="Choose your mode",
            previous_view=previous_view
        )

        button_25_words = self.create_button("25 Words")
        @button_25_words.event("on_click")
        def _(event: "UIOnClickEvent") -> None:
            """
            Start the game with 25 words.
            """
            self.start_game(25)

        button_50_words = self.create_button("50 Words")
        @button_50_words.event("on_click")
        def _(event: "UIOnClickEvent") -> None:
            """
            Start the game with 50 words.
            """
            self.start_game(50)

        button_100_words = self.create_button("100 Words")
        @button_100_words.event("on_click")
        def _(event: "UIOnClickEvent") -> None:
            """
            Start the game with 100 words.
            """
            self.start_game(100)

        button_back = self.create_button("Back")
        @button_back.event("on_click")
        def _(event: "UIOnClickEvent") -> None:
            """
            Return to the previous view.
            """
            self.return_to_previous_view()

        button_stats = self.create_button("Stats")
        @button_stats.event("on_click")
        def _(event: "UIOnClickEvent") -> None:
            """
            Show the stats view.
            """
            stats_view = StatsView(self)
            self.window.show_view(stats_view)

        self.initialize_buttons(
            [
                button_25_words,
                button_50_words,
                button_100_words,
                button_stats,
                button_back,
            ]
        )
    
    def start_game(self, words_count: int) -> None:
        """
        Start the game.
        """
        ai_trainer_view = AITrainerView(self.main_menu_view, words_count)
        self.window.show_view(ai_trainer_view)

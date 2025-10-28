import arcade
from utils.word_manager import WordManager
from utils.resources import SEPIA_BACKGROUND
from utils.colors import BROWN
from pyglet.graphics import Batch
from ai_trainer.input_text_manager import InputTextManager
from ai_trainer.session_stats import SessionStats
from utils.menu_view import MenuView
from utils.save_manager import SaveManager
from utils import global_state
from utils.resources import AI_TRAINER_MUSIC
from utils.music_manager import MusicManager


class AITrainerView(arcade.View):

    TARGET_TEXT_COLOR = BROWN
    INPUT_TEXT_COLOR = arcade.color.ANTIQUE_BRASS
    WPM_TEXT_COLOR = arcade.color.ANTIQUE_RUBY
    FONT_NAME = "Pixelzone"
    WORD_CHARACTER_COUNT_MIN = 4
    WORD_CHARACTER_COUNT_MAX = 8

    def __init__(self, main_menu_view, words_count):
        super().__init__()
        self.background = SEPIA_BACKGROUND
        self.main_menu_view = main_menu_view
        self.words_count = words_count
        self.user_profile = global_state.current_user_profile
        self.word_manager = WordManager()
        self.input_text_manager = InputTextManager()
        self.session_stats = SessionStats()
        self.text_batch = Batch()
        self.target_text = arcade.Text(
            "", 
            x=self.window.width//2, 
            y=self.window.height//2 + 100, 
            anchor_x="center",
            font_name=self.FONT_NAME,
            font_size=64,
            color=self.TARGET_TEXT_COLOR,
            bold=True,
            batch=self.text_batch
        )
        self.next_word_text = arcade.Text(
            "", 
            x=self.target_text.x, 
            y=self.target_text.y - 60, 
            anchor_x="center",
            font_name=self.FONT_NAME,
            font_size=36,
            color=self.TARGET_TEXT_COLOR,
            batch=self.text_batch
        )
        self.input_text = arcade.Text(
            "", 
            x=self.target_text.x, 
            y=self.target_text.y - 150, 
            anchor_x="center",
            font_name=self.FONT_NAME,
            font_size=64,
            color=self.INPUT_TEXT_COLOR,
            batch=self.text_batch
        )
        self.wpm_text = arcade.Text(
            "",
            x=self.window.width//2,
            y=20,
            anchor_x="center",
            font_name="Pixelzone",
            font_size=50,
            color=self.WPM_TEXT_COLOR,
            batch=self.text_batch
        )
        self.typing_sound = arcade.Sound("assets/sounds/eklee-KeyPressMac06.wav")
        self.setup()

    def setup(self):
        self.target_text.text = self.word_manager.generate_word(
            min_character_count=self.WORD_CHARACTER_COUNT_MIN, 
            max_character_count=self.WORD_CHARACTER_COUNT_MAX
        )
        self.next_word_text.text = self.word_manager.generate_word(
            min_character_count=self.WORD_CHARACTER_COUNT_MIN, 
            max_character_count=self.WORD_CHARACTER_COUNT_MAX
        )
        self.input_text.text = ""
        self.input_text_manager.set_target_text(self.target_text.text)
        MusicManager.play_music(AI_TRAINER_MUSIC)
    
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            SEPIA_BACKGROUND,
            arcade.LBWH(0, 0, self.window.width, self.window.height)
        )
        self.text_batch.draw()

    def on_update(self, delta_time):
        self.session_stats.duration_seconds += delta_time
        self.input_text.text = self.input_text_manager.input_text
        if self.input_text_manager.is_input_matching_target():
            self.target_text.text = self.next_word_text.text
            self.next_word_text.text = self.word_manager.generate_word(
                min_character_count=self.WORD_CHARACTER_COUNT_MIN,
                max_character_count=self.WORD_CHARACTER_COUNT_MAX
            )
            self._update_metrics()
            if self.session_stats.words_typed >= self.words_count:
                self._complete_game()
            self.input_text_manager.set_target_text(self.target_text.text)
        self._update_wpm_text()

    def _update_metrics(self):
        self.session_stats.words_typed += 1
        count_correct = len(self.input_text_manager.target_text)
        count_total = 0
        for char_expected, counts in self.input_text_manager.char_confusion_matrix.items():
            for char_actual, count in counts.items():
                self.session_stats.char_confusion_matrix[char_expected][char_actual] += count
                count_total += count
        self.session_stats.chars_typed_correctly += count_correct
        self.session_stats.chars_typed_total += count_total
        self._update_wpm()
    
    def _update_wpm(self):
        if self.session_stats.duration_seconds >= 2:
            self.session_stats.wpm = int(
                self.session_stats.chars_typed_correctly * 12 / self.session_stats.duration_seconds
            )
        if self.session_stats.chars_typed_total > 0:
            self.session_stats.accuracy = 100.0 * \
                self.session_stats.chars_typed_correctly / self.session_stats.chars_typed_total
        
    def _update_wpm_text(self):
        self.wpm_text.text = f"WPM: {self.session_stats.wpm}, " + \
            f"Accuracy: {self.session_stats.accuracy:.2f}%"
        
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            pause_view = PauseView(self, self.session_stats)
            self.window.show_view(pause_view)
        else:
            self._play_typing_sound()

    def _complete_game(self):
        game_completed_view = GameCompletedView(self, self.session_stats)
        self.window.show_view(game_completed_view)

    def _play_typing_sound(self):
        arcade.play_sound(self.typing_sound, volume=0.75)

    def on_text(self, text):
        """
        Captures unicode text input after applying modifiers.
        This works (even though it's not mentioned in arcade's documentation) 
        because arcade probably inherits pyglet.window
        """
        if text not in {'\r', '\n', '\r\n'}:
            self.input_text_manager.capture_character_input(text)
            self.input_text.text = self.input_text_manager.input_text
            
    def on_text_motion(self, motion):
        """
        Identifying when the backspace key is pressed (or held pressed)
        """
        if motion == arcade.key.MOTION_BACKSPACE:
            self.input_text_manager.capture_backspace()
    
    def on_show_view(self):
        self.window.set_mouse_visible(False)

    def on_hide_view(self):
        self.window.set_mouse_visible(True)


class PauseView(MenuView):

    def __init__(self, game_view, session_stats):
        self.game_view = game_view
        self.save_manager = SaveManager(global_state.current_user_profile)
        self.session_stats = session_stats
        self.TITLE_OFFSET_FROM_CENTER = 100
        self.TITLE_FONT_SIZE = 64
        score_text = f"WPM: {self.session_stats.wpm}," + \
            f" Words typed: {self.session_stats.words_typed}, " + \
            f" Accuracy: {self.session_stats.accuracy:.2f}%"
        super().__init__(
            title_text="Game Paused",
            subtitle_text=score_text
        )

        resume_button = self.create_button("Resume")
        @resume_button.event("on_click")
        def _(event):
            self._resume()

        quit_to_main_menu_button = self.create_button("Quit to Main Menu")
        @quit_to_main_menu_button.event("on_click")
        def _(event):
            self._return_to_main_menu()

        self.initialize_buttons(
            [
                resume_button,
                quit_to_main_menu_button
            ]
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self._resume()

    def _resume(self):
        self.window.show_view(self.game_view)

    def _return_to_main_menu(self):
        self.save_manager.save_session_stats_to_db(self.session_stats)
        self.save_manager.load_and_print_db()
        self.window.show_view(self.game_view.main_menu_view)


class GameCompletedView(MenuView):

    def __init__(self, game_view, session_stats):
        self.game_view = game_view
        self.save_manager = SaveManager(global_state.current_user_profile)
        self.session_stats = session_stats
        self.TITLE_OFFSET_FROM_CENTER = 100
        self.TITLE_FONT_SIZE = 64
        score_text = f"WPM: {self.session_stats.wpm}," + \
            f" Words typed: {self.session_stats.words_typed}, " + \
            f" Accuracy: {self.session_stats.accuracy:.2f}%"
        super().__init__(
            title_text="Session Completed!",
            subtitle_text=score_text
        )

        continue_button = self.create_button("Continue")
        @continue_button.event("on_click")
        def _(event):
            self._return_to_main_menu()

        self.initialize_buttons(
            [
                continue_button
            ]
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self._return_to_main_menu()

    def _return_to_main_menu(self):
        self.save_manager.save_session_stats_to_db(self.session_stats)
        self.save_manager.load_and_print_db()
        self.window.show_view(self.game_view.main_menu_view)


class ModeSelectionView(MenuView):

    def __init__(self, previous_view, main_menu_view):
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
        def _(event):
            self.start_game(25)

        button_50_words = self.create_button("50 Words")
        @button_50_words.event("on_click")
        def _(event):
            self.start_game(50)

        button_100_words = self.create_button("100 Words")
        @button_100_words.event("on_click")
        def _(event):
            self.start_game(100)

        button_back = self.create_button("Back")
        @button_back.event("on_click")
        def _(event):
            self.return_to_previous_view()

        self.initialize_buttons(
            [
                button_25_words,
                button_50_words,
                button_100_words,
                button_back
            ]
        )
    
    def start_game(self, words_count):
        ai_trainer_view = AITrainerView(self.main_menu_view, words_count)
        self.window.show_view(ai_trainer_view)

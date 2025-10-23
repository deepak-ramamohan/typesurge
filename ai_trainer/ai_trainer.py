import arcade
from space_shooter.word_manager import WordManager
from utils.textures import SEPIA_BACKGROUND
from utils.colors import BROWN
from pyglet.graphics import Batch
from arcade.gui import (
    UIManager,
    UIAnchorLayout,
    UIFlatButton,
    UIBoxLayout
)
from utils.button_styles import sepia_button_style
from collections import defaultdict


class AITrainerView(arcade.View):

    TARGET_TEXT_COLOR = BROWN
    INPUT_TEXT_COLOR = arcade.color.ANTIQUE_BRASS
    WPM_TEXT_COLOR = arcade.color.ANTIQUE_RUBY
    FONT_NAME = "Pixelzone"
    WORD_CHARACTER_COUNT_MIN = 4
    WORD_CHARACTER_COUNT_MAX = 8

    def __init__(self, main_menu_view):
        super().__init__()
        self.background = SEPIA_BACKGROUND
        self.main_menu_view = main_menu_view
        self.word_manager = WordManager()
        self.input_text_manager = InputTextManager()
        self.typing_metrics_tracker = TypingMetricsTracker()
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
        self.game_music = arcade.Sound("assets/sounds/vibing_over_venus.mp3", streaming=True)
        self.current_music = None

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
        self.typing_metrics_tracker.reset_metrics()
        self.current_music = arcade.play_sound(self.game_music, loop=True)
    
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            SEPIA_BACKGROUND,
            arcade.LBWH(0, 0, self.window.width, self.window.height)
        )
        self.text_batch.draw()

    def on_update(self, delta_time):
        self.input_text.text = self.input_text_manager.input_text
        self.typing_metrics_tracker.update_time(delta_time)
        if self.input_text_manager.is_input_matching_target():
            self.target_text.text = self.next_word_text.text
            self.next_word_text.text = self.word_manager.generate_word(
                min_character_count=self.WORD_CHARACTER_COUNT_MIN,
                max_character_count=self.WORD_CHARACTER_COUNT_MAX
            )
            self.typing_metrics_tracker.update_metrics(self.input_text_manager)
            self.input_text_manager.set_target_text(self.target_text.text)
        self._update_wpm_text()
        
    def _update_wpm_text(self):
        self.wpm_text.text = f"WPM: {self.typing_metrics_tracker.wpm}, " + \
            f"Accuracy: {self.typing_metrics_tracker.accuracy:.2f}%"
        
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)
        else:
            self._play_typing_sound()

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
            # print(
            #     self.input_text_manager._caret,
            #     self.input_text_manager.text_input_buffer,
            #     self.input_text_manager.char_confusion_matrix
            # )
            
    def on_text_motion(self, motion):
        """
        Identifying when the backspace key is pressed (or held pressed)
        """
        if motion == arcade.key.MOTION_BACKSPACE:
            self.input_text_manager.capture_backspace()
            # print(
            #     self.input_text_manager._caret,
            #     self.input_text_manager.text_input_buffer,
            #     self.input_text_manager.char_confusion_matrix
            # )
    
    def on_show_view(self):
        self.window.set_mouse_visible(False)
        if self.current_music:
            self.current_music.play()

    def on_hide_view(self):
        self.window.set_mouse_visible(True)
        # if self.current_music:
        #     self.current_music.pause()


class InputTextManager():

    def __init__(self):
        self.target_text = ""
        self.reset_input()

    def capture_character_input(self, input):
        self.text_input_buffer.append(input)
        if self._caret < len(self.target_text):
            correct_char = self.target_text[self._caret]
            self.char_confusion_matrix[correct_char][input] += 1
        self._caret += 1

    def capture_backspace(self):
        if self._caret > 0:
            self._caret -= 1
        if self.text_input_buffer:
            self.text_input_buffer.pop()

    def reset_input(self):
        self.text_input_buffer = []
        self._caret = 0
        self.char_confusion_matrix = defaultdict(lambda: defaultdict(int))

    def set_target_text(self, target_text):
        self.target_text = target_text
        self.reset_input()

    def is_input_matching_target(self):
        if self._caret < len(self.target_text):
            return False
        return ''.join(self.text_input_buffer) == self.target_text
    
    @property
    def input_text(self):
        return ''.join(self.text_input_buffer)
    

class TypingMetricsTracker():
    """
    Class for tracking metrics such as WPM, CPM and Accuracy
    """

    def __init__(self):
        self.wpm = 0
        self.time_elapsed = 0
        self.words_typed_correctly = 0
        self.characters_typed_correctly = 0
        self.characters_typed_total = 0
        self.accuracy = 0.0

    def update_metrics(self, input_text_manager):
        self.words_typed_correctly += 1
        count_correct = len(input_text_manager.target_text)
        count_total = 0
        for _, counts in input_text_manager.char_confusion_matrix.items():
            count_total += sum(counts.values())
        self.characters_typed_correctly += count_correct
        self.characters_typed_total += count_total
        self._update_wpm()

    def update_time(self, delta_time):
        self.time_elapsed += delta_time

    def reset_metrics(self):
        self.wpm = 0
        self.accuracy = 0.0
        self.characters_typed_correctly = 0
        self.characters_typed_total = 0
        self.time_elapsed = 0
        self._update_wpm()

    def _update_wpm(self):
        if self.time_elapsed >= 2:
            self.wpm = int(self.characters_typed_correctly * 12 / self.time_elapsed)
        if self.characters_typed_total > 0:
            self.accuracy = 100.0 * self.characters_typed_correctly / self.characters_typed_total


class PauseView(arcade.View):

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.text_batch = Batch()
        self.title_text = arcade.Text(
            "Game Paused",
            x = self.window.width // 2,
            y = self.window.height // 2 + 100,
            anchor_x="center",
            font_name=self.game_view.FONT_NAME,
            font_size=64,
            color=BROWN,
            bold=True,
            batch=self.text_batch
        )
        score_text = f"WPM: {self.game_view.typing_metrics_tracker.wpm}," + \
            f" Words typed: {self.game_view.typing_metrics_tracker.words_typed_correctly}, " + \
            f" Accuracy: {self.game_view.typing_metrics_tracker.accuracy:.2f}%"
        self.score_text = arcade.Text(
            score_text,
            x = self.title_text.x,
            y = self.title_text.y - 70,
            anchor_x="center",
            font_name=self.game_view.FONT_NAME,
            font_size=48,
            color=BROWN,
            batch=self.text_batch
        )

        self.ui = UIManager()
        self.anchor = self.ui.add(UIAnchorLayout())
        self.BUTTON_WIDTH = 300

        self.resume_button = UIFlatButton(
            text="Resume",
            width=self.BUTTON_WIDTH,
            style=sepia_button_style
        )
        @self.resume_button.event("on_click")
        def _(event):
            self._resume()

        self.quit_to_main_menu_button = UIFlatButton(
            text="Quit to Main Menu",
            width=self.BUTTON_WIDTH,
            style=sepia_button_style
        )
        @self.quit_to_main_menu_button.event("on_click")
        def _(event):
            self._return_to_main_menu()

        self.box_layout = UIBoxLayout(space_between=15)
        self.box_layout.add(self.resume_button)
        self.box_layout.add(self.quit_to_main_menu_button)
        self.anchor.add(
            self.box_layout,
            anchor_y="top",
            align_y=-(self.height - self.score_text.y + 30)
        )

    def on_show_view(self):
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_draw(self):
        self.clear() # This is IMPORTANT! The text looks jagged without this!
        arcade.draw_texture_rect(
            SEPIA_BACKGROUND,
            arcade.LBWH(0, 0, self.window.width, self.window.height)
        )
        self.text_batch.draw()
        self.ui.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self._resume()

    def _resume(self):
        self.window.show_view(self.game_view)

    def _return_to_main_menu(self):
        if self.game_view.current_music:
            self.game_view.current_music.pause()
        self.window.show_view(self.game_view.main_menu_view)
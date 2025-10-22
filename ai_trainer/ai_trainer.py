import arcade
import random
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
        self.text_input_buffer = []
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
        self.wpm = 0
        self.time_elapsed = 0
        self.words_typed = 0
        self.character_count = 0
        self.typing_sound = arcade.Sound("assets/sounds/eklee-KeyPressMac06.wav")

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
        self._reset_wpm()
    
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            SEPIA_BACKGROUND,
            arcade.LBWH(0, 0, self.window.width, self.window.height)
        )
        self.text_batch.draw()

    def on_update(self, delta_time):
        self.input_text.text = ''.join(self.text_input_buffer)
        if self._is_input_matching():
            self.character_count += len(self.text_input_buffer)
            self.text_input_buffer = []
            self.target_text.text = self.next_word_text.text
            self.next_word_text.text = self.word_manager.generate_word(
                min_character_count=self.WORD_CHARACTER_COUNT_MIN,
                max_character_count=self.WORD_CHARACTER_COUNT_MAX
            )
            self.words_typed += 1
        self._update_wpm(delta_time)

    def _reset_wpm(self):
        self.wpm = 0
        self.character_count = 0
        self.time_elapsed = 0
        self._update_wpm(0)

    def _update_wpm(self, delta_time):
        self.time_elapsed += delta_time
        if self.time_elapsed >= 2:
            self.wpm = int(self.character_count * 12 / self.time_elapsed)
        self.wpm_text.text = f"WPM: {self.wpm}"
        
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
            self.text_input_buffer.append(text)
            
    def on_text_motion(self, motion):
        """
        Identifying when the backspace key is pressed (or held pressed)
        """
        if motion == arcade.key.MOTION_BACKSPACE and self.text_input_buffer:
            self.text_input_buffer.pop()

    def _is_input_matching(self):
        return self.input_text.text == self.target_text.text
    
    def on_show_view(self):
        self.window.set_mouse_visible(False)

    def on_hide_view(self):
        self.window.set_mouse_visible(True)


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
        self.score_text = arcade.Text(
            f"WPM: {self.game_view.wpm}, Words typed: {self.game_view.words_typed}", 
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
        self.window.show_view(self.game_view.main_menu_view)
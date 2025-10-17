import arcade
from space_shooter.word_manager import WordManager


class AITrainerView(arcade.View):

    BACKGROUND_COLOR = arcade.color.ANTIQUE_WHITE
    TARGET_TEXT_COLOR = arcade.color.BAZAAR
    INPUT_TEXT_COLOR = arcade.color.ANTIQUE_BRASS
    WPM_TEXT_COLOR = arcade.color.ANTIQUE_RUBY

    def __init__(self, main_menu_view):
        super().__init__(background_color=self.BACKGROUND_COLOR)
        self.main_menu_view = main_menu_view
        self.word_manager = WordManager()
        self.text_input_buffer = []
        self.target_text = arcade.Text(
            "", 
            x=self.window.width//2, 
            y=self.window.height//2 + 50, 
            anchor_x="center",
            font_size=36,
            color=self.TARGET_TEXT_COLOR
        )
        self.input_text = arcade.Text(
            "", 
            x=self.target_text.x, 
            y=self.target_text.y - 80, 
            anchor_x="center",
            font_size=36,
            color=self.INPUT_TEXT_COLOR
        )
        self.wpm_text = arcade.Text(
            "",
            x=10,
            y=15,
            font_size=28,
            color=self.WPM_TEXT_COLOR
        )
        self.wpm = 0
        self.time_elapsed = 0
        self.character_count = 0

    def setup(self):
        self.target_text.text = self.word_manager.generate_word(min_character_count=4, max_character_count=8)
        self.input_text.text = ""
        self._reset_wpm()
    
    def on_draw(self):
        self.clear()
        self.target_text.draw()
        self.input_text.draw()
        self.wpm_text.draw()

    def on_update(self, delta_time):
        self.input_text.text = ''.join(self.text_input_buffer)
        if self._is_input_matching():
            self.character_count += len(self.text_input_buffer)
            self.text_input_buffer = []
            self.target_text.text = self.word_manager.generate_word(min_character_count=4, max_character_count=8)
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
            self.window.show_view(self.main_menu_view)

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

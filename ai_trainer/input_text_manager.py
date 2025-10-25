from collections import defaultdict


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

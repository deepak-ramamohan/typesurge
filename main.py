import arcade
import random
from pyglet.graphics import Batch

class GameView(arcade.Window):
    
    def __init__(self, width = 1280, height = 720, title = "Typing Game"):
        super().__init__(width, height, title)

        self.player_sprite = None
        self.text_box = None
        self.current_word = ""
        self.input = ""
        self.laser_sound = arcade.Sound(":resources:/sounds/hit2.wav")

    def setup(self):
        self.player_sprite = arcade.Sprite(":resources:/images/space_shooter/playerShip1_blue.png", angle=90)
        self.player_sprite.position = [100, self.height // 2]
        self.current_word = self._get_word()
        self.input = ""
        self.laser_list = arcade.SpriteList()
        self.enemy_word = Word(self.current_word, 800, 360)

    def on_draw(self):
        self.clear()
        self.laser_list.draw()
        arcade.draw_sprite(self.player_sprite)
        self.enemy_word.draw()

    def _fire_laser(self):
        laser = arcade.Sprite(":resources:/images/space_shooter/laserBlue01.png")
        laser.center_y = self.player_sprite.center_y
        laser.left = self.player_sprite.right
        laser.change_x = 40
        self.laser_list.append(laser)
        arcade.play_sound(self.laser_sound)

    def _update_laser(self):
        self.laser_list.update()
        for laser in self.laser_list:
            if laser.left > self.width:
                laser.remove_from_sprite_lists()

    def on_update(self, delta_time):
        self._update_laser()
        match = self.enemy_word.match(self.input)
        if match == "mismatch":
            self.input = ""
        elif match == "full":
            self.input = ""
            self._fire_laser()
            self.current_word = self._get_word()
            self.enemy_word = Word(self.current_word, 800, 360)
            
    def on_key_press(self, symbol, modifiers):
        key_mapping = {
            arcade.key.A: "a",
            arcade.key.B: "b",
            arcade.key.C: "c",
            arcade.key.D: "d",
            arcade.key.E: "e",
            arcade.key.F: "f",
            arcade.key.G: "g",
            arcade.key.H: "h",
            arcade.key.I: "i",
            arcade.key.J: "j",
            arcade.key.K: "k",
            arcade.key.L: "l",
            arcade.key.M: "m",
            arcade.key.N: "n",
            arcade.key.O: "o",
            arcade.key.P: "p",
            arcade.key.Q: "q",
            arcade.key.R: "r",
            arcade.key.S: "s",
            arcade.key.T: "t",
            arcade.key.U: "u",
            arcade.key.V: "v",
            arcade.key.W: "w",
            arcade.key.X: "x",
            arcade.key.Y: "y",
            arcade.key.Z: "z",
            arcade.key.COMMA: ",",
            arcade.key.PERIOD: ".",
            arcade.key.SLASH: "/",
            arcade.key.COLON: ";",
            arcade.key.QUOTELEFT: "'",
            arcade.key.BRACKETLEFT: "[",
            arcade.key.BRACKETRIGHT: "]"
        }
        key_pressed = key_mapping.get(symbol, "")
        self.input = self.input + key_pressed

    def _get_word(self):
        word_list = ["hello", "world", "the", "quick", "brown", "fox", "jumps",
                     "over", "lazy", "dog"]
        return random.choice(word_list)
    

class Word:
    """
    Requirements:

    1. Each word consists of individual characters
    2. We need to partially match the user input with the word (example: "hel" matches "hello" partially)
    3. We need to color the partially matched characters separately (e.g., in red)
    4. We need to draw and update the characters on the screen

    """

    def __init__(self, word, x, y, 
                 matched_color=arcade.color.RED_ORANGE, 
                 unmatched_color=arcade.color.WHITE, font_size=24):
        self.word = word
        self.matched_color = matched_color
        self.unmatched_color = unmatched_color
        self.characters = [c for c in word]
        self.batch = Batch()
        self.text_list = []
        for c in self.characters:
            text = arcade.Text(c, x, y, color=unmatched_color, font_size=font_size, batch=self.batch)
            x = text.right
            self.text_list.append(text)

    def match(self, other):
        for i, c in enumerate(other):
            if i >= len(self.characters) or self.characters[i] != c:
                self.reset_color()
                return "mismatch"
            self.text_list[i].color = self.matched_color
        if len(self.characters) == len(other):
            return "full"
        return "partial"
    
    def reset_color(self):
        for text in self.text_list:
            text.color = self.unmatched_color
    
    def draw(self):
        self.batch.draw()


def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
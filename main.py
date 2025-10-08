import arcade
import random
from pyglet.graphics import Batch


class GameView(arcade.Window):
    
    def __init__(self, width = 1280, height = 720, title = "Typing Game"):
        super().__init__(width, height, title)
        self.player_sprite = None
        self.input = ""
        self.explosion_list = None
        self._load_explosion_texture_list()
        self.laser_sound = arcade.Sound(":resources:/sounds/laser2.wav")
        self.explosion_sound = arcade.Sound(":resources:/sounds/explosion2.wav")
        self.game_over_sound = arcade.Sound(":resources:/sounds/gameover3.wav")
        self.SOUND_VOLUME = 1.0
        # For fixing the initial sound distortion, play something at zero volume
        # Subsequent sounds will then play clearly
        arcade.play_sound(self.laser_sound, volume=0)

    def setup(self):
        self.player_sprite = arcade.Sprite(":resources:/images/space_shooter/playerShip1_blue.png", angle=90)
        self.player_sprite.position = [75, self.height // 2]
        self.input = ""
        self.laser_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()
        self.enemy_word_list = EnemyWordList()
        enemy_word = EnemyWord(self._get_word(), 800, 360)
        self.enemy_word_list.append(enemy_word)

    def on_draw(self):
        self.clear()
        self.laser_list.draw()
        arcade.draw_sprite(self.player_sprite)
        self.enemy_word_list.draw()
        self.explosion_list.draw()

    def _fire_laser(self):
        laser = arcade.Sprite(":resources:/images/space_shooter/laserBlue01.png")
        laser.center_y = self.player_sprite.center_y
        laser.left = self.player_sprite.right
        laser.change_x = 40
        self.laser_list.append(laser)
        arcade.play_sound(self.laser_sound, volume=self.SOUND_VOLUME)

    def _load_explosion_texture_list(self):
        spritesheet = arcade.load_spritesheet(":resources:images/spritesheets/explosion.png")
        self.explosion_texture_list = spritesheet.get_texture_grid(
            size=(256, 256),
            columns=16,
            count=16*10
        )

    def _create_explosion_at_position(self, position):
        explosion = Explosion(self.explosion_texture_list)
        explosion.position = position
        # explosion.update()
        self.explosion_list.append(explosion)

    def _update_laser(self):
        self.laser_list.update()
        for laser in self.laser_list:
            if laser.left > self.width:
                laser.remove_from_sprite_lists()
            collisions = arcade.check_for_collision_with_list(laser, self.enemy_word_list)
            if collisions:
                laser.remove_from_sprite_lists()
                arcade.play_sound(self.explosion_sound, volume=self.SOUND_VOLUME)
                for enemy_word in collisions:
                    self._create_explosion_at_position(enemy_word.position)
                    enemy_word.remove_from_sprite_lists()

    def _check_player_collision(self):
        collisions = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_word_list)
        if collisions:
            arcade.play_sound(self.game_over_sound)
            self.setup()

    def on_update(self, delta_time):
        self._check_player_collision()
        self._update_laser()
        self.explosion_list.update(delta_time=delta_time)
        self.enemy_word_list.update(delta_time=delta_time)
        for enemy_word in self.enemy_word_list:
            matching_result = enemy_word.match_text(self.input)
            if matching_result == "mismatch":
                self.input = ""
            elif matching_result == "full":
                self.input = ""
                self._fire_laser()
                next_word = self._get_word()
                self.enemy_word_list.append(EnemyWord(next_word, 800, 360))
            
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
    

class EnemyWord(arcade.Sprite):
    """
    Requirements:
    1. Each word consists of individual characters
    2. We need to partially match the user input with the word (example: "hel" matches "hello" partially)
    3. We need to color the partially matched characters separately (e.g., in red)
    4. We need to draw and update the text characters on the screen

    """

    def __init__(
        self, 
        word, 
        x, 
        y, 
        MATCHED_COLOR=arcade.color.RED_ORANGE, 
        UNMATCHED_COLOR=arcade.color.WHITE, 
        font_size=24
    ):
        self.MATCHED_COLOR = MATCHED_COLOR
        self.UNMATCHED_COLOR = UNMATCHED_COLOR
        self.METEOR_SPRITES = [
            ":resources:/images/space_shooter/meteorGrey_med1.png",
            ":resources:/images/space_shooter/meteorGrey_med2.png"
        ]
        self.meteor_sprite = random.choice(self.METEOR_SPRITES)
        super().__init__(self.meteor_sprite, center_x=x, center_y=y)
        self.change_x = -1.5
        self.WORD_OFFSET_PIXELS = 5
        self.word = word
        self.text_characters = [c for c in word]
        self.text_batch = Batch()
        self.text_list = []
        # Update coordinates
        x = self.right + self.WORD_OFFSET_PIXELS
        for c in self.text_characters:
            text = arcade.Text(c, x, y, color=UNMATCHED_COLOR, font_size=font_size, batch=self.text_batch, anchor_y='center')
            x = text.right
            self.text_list.append(text)

    def update(self, delta_time = 1 / 60):
        super().update(delta_time=delta_time)
        self._update_text_character_positions()

    def _update_text_character_positions(self):
        x, y = self.right + self.WORD_OFFSET_PIXELS, self.center_y
        for text in self.text_list:
            text.x, text.y = x, y
            x = text.right

    def match_text(self, other):
        for i, c in enumerate(other):
            if i >= len(self.text_characters) or self.text_characters[i] != c:
                self.reset_color()
                return "mismatch"
            self.text_list[i].color = self.MATCHED_COLOR
        if len(self.text_characters) == len(other):
            return "full"
        return "partial"
    
    def reset_color(self):
        for text in self.text_list:
            text.color = self.UNMATCHED_COLOR
    
    def draw(self):
        self.text_batch.draw()
        arcade.draw_sprite(self)


class EnemyWordList(arcade.SpriteList):

    def __init__(self, use_spatial_hash = False, spatial_hash_cell_size = 128, atlas = None, capacity = 100, lazy = False, visible = True):
        super().__init__(use_spatial_hash, spatial_hash_cell_size, atlas, capacity, lazy, visible)

    def draw(self):
        for enemy_word in self:
            arcade.draw_sprite(enemy_word)
            enemy_word.text_batch.draw()


class Explosion(arcade.Sprite):

    def __init__(self, texture_list):
        super().__init__(texture_list[0])
        self.time_elapsed = 0
        self.animation_time = 0.6
        self.textures = texture_list

    def update(self, delta_time = 1 / 60):
        self.time_elapsed += delta_time
        if self.time_elapsed <= self.animation_time:
            index = int(len(self.textures) * (self.time_elapsed / self.animation_time))
            self.set_texture(index)
        else:
            self.remove_from_sprite_lists()


def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
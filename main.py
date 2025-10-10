import arcade
from arcade.clock import GLOBAL_CLOCK
import random
import math
import numpy as np
from pyglet.graphics import Batch
from collections import defaultdict


class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()
        self.enemy_spawner = EnemySpawner()
        self.player_sprite = None
        self.input = ""
        self.explosion_list = None
        self.score = 0
        self.score_text = arcade.Text("", 10, 15, font_size=20, bold=True)
        self._load_explosion_texture_list()
        self.ENEMY_COUNT_MIN = 2
        self.ENEMY_COUNT_MAX = 5
        self.LASER_SPEED = 40
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
        self.score = 0
        self._update_score_text()
        self.laser_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()
        self.enemy_word_list = EnemyWordList()

    def on_draw(self):
        self.clear()
        self.laser_list.draw()
        arcade.draw_sprite(self.player_sprite)
        self.enemy_word_list.draw()
        self.explosion_list.draw()
        self.score_text.draw()

    def _spawn_enemies(self):
        """
        Keep spawning enemies to ensure that the count is between ENEMY_COUNT_MIN and ENEMY_COUNT_MAX
        """
        current_enemy_count = len(self.enemy_word_list)
        count_target = self.ENEMY_COUNT_MIN if random.random() <= 0.8 else self.ENEMY_COUNT_MAX
        while current_enemy_count < count_target:
            enemy_word = self.enemy_spawner.spawn_enemy(
                player_position=self.player_sprite.position,
                window_width=self.width,
                window_height=self.height
            )
            self.enemy_word_list.append(enemy_word)
            current_enemy_count += 1    

    def _fire_laser_at(self, enemy_word):
        laser = arcade.Sprite(":resources:/images/space_shooter/laserBlue01.png")
        laser.center_y = self.player_sprite.center_y
        laser.left = self.player_sprite.right
        theta = calculate_angle(laser.position, enemy_word.position)
        laser.velocity = [self.LASER_SPEED * math.cos(theta), self.LASER_SPEED * math.sin(theta)]
        laser.angle = math.degrees(2 * math.pi - theta)
        self.laser_list.append(laser)
        arcade.play_sound(self.laser_sound, volume=self.SOUND_VOLUME)
        enemy_word.reset_color()

    def _load_explosion_texture_list(self):
        spritesheet = arcade.load_spritesheet(":resources:images/spritesheets/explosion.png")
        self.explosion_texture_list = spritesheet.get_texture_grid(
            size=(256, 256),
            columns=16,
            count=16*10
        )

    def _create_explosions_at_sprites(self, sprites_list: list[arcade.Sprite]) -> None:
        for sprite in sprites_list:
            arcade.play_sound(self.explosion_sound, volume=self.SOUND_VOLUME)
            explosion = Explosion(self.explosion_texture_list)
            explosion.position = sprite.position
            self.explosion_list.append(explosion)
            sprite.remove_from_sprite_lists()

    def _add_scores_from_words(self, enemy_words):
        for enemy_word in enemy_words:
            self.score += 20 * len(enemy_word.word)
        self._update_score_text()

    def _check_laser_collisions(self, delta_time):
        self.laser_list.update()
        for laser in self.laser_list:
            if laser.left > self.width:
                laser.remove_from_sprite_lists()
            collisions = arcade.check_for_collision_with_list(laser, self.enemy_word_list)
            if collisions:
                laser.remove_from_sprite_lists()
                self._add_scores_from_words(collisions)
                self._create_explosions_at_sprites(collisions)

    def _check_player_collision(self):
        collisions = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_word_list)
        if collisions:
            self._create_explosions_at_sprites(collisions)
            # TO BE UPDATED
            # For now, show game over screen even if a single word hits the player
            game_over_view = GameOverView(self.score)
            self.window.show_view(game_over_view)

    def _check_word_matches(self):
        mismatch_count = 0
        full_match_count = 0
        for enemy_word in self.enemy_word_list:
            matching_result = enemy_word.match_text(self.input)
            if matching_result == "mismatch":
                mismatch_count += 1
            elif matching_result == "full":
                full_match_count += 1
                self._fire_laser_at(enemy_word)
        # If none of the words matches or there are full matches, reset the input
        if mismatch_count == len(self.enemy_word_list) or full_match_count > 0:
            self.input = ""

    def on_update(self, delta_time):
        self._check_player_collision()
        self._check_laser_collisions(delta_time=delta_time)
        self.explosion_list.update(delta_time=delta_time)
        self.enemy_word_list.update(delta_time=delta_time)
        self._check_word_matches()
        self._spawn_enemies()

    def _update_score_text(self):
        self.score_text.text = f"Score: {self.score}"
            
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)
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
        position,
        target_position, 
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
        x, y = position
        super().__init__(self.meteor_sprite, center_x=x, center_y=y)
        self.movement_speed = random.uniform(0.75, 1.25) # This needs to be a configuration in the future
        self.change_angle = random.uniform(-5.0, 5.0)
        theta = calculate_angle(position, target_position)
        self.velocity = [self.movement_speed * math.cos(theta), self.movement_speed * math.sin(theta)]
        self.WORD_OFFSET_PIXELS = 35
        self.word = word
        self.text_characters = [c for c in word]
        self.text_batch = Batch()
        self.text_list = []
        for c in self.text_characters:
            text = arcade.Text(c, x, y, color=UNMATCHED_COLOR, font_size=font_size, batch=self.text_batch, anchor_y='center')
            self.text_list.append(text)
        self._update_text_character_positions()

    def update(self, delta_time = 1 / 60):
        super().update(delta_time=delta_time)
        self._update_text_character_positions()

    def _update_text_character_positions(self):
        x, y = self.center_x + self.WORD_OFFSET_PIXELS, self.center_y
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


class EnemySpawner():

    def __init__(self):
        self.word_manager = WordManager()
        self.ANGLE_RANGE_DEGREES = 45
        self.OFFSCREEN_SPAWN_OFFSET_PIXELS = 30
        self.SPAWN_POINTS_COUNT = 9  # Number of distinct spawn points
        self.spawn_angles = np.linspace(
            -self.ANGLE_RANGE_DEGREES/2, 
            self.ANGLE_RANGE_DEGREES/2,
            self.SPAWN_POINTS_COUNT
        )
        self.SPAWN_COOLDOWN_SECONDS = 5
        self.recently_spawned = {}  # key: point index, value: spawn time
        self.available_indexes = set(range(self.SPAWN_POINTS_COUNT))

    def _get_spawn_angle(self):
        self._update_available_indexes()
        # Choose from one of the available points (if exists)
        if len(self.available_indexes) > 0:
            idx = random.choice(list(self.available_indexes))
            # Remove from available indexes
            self.available_indexes.remove(idx)
        else:
            idx = random.choice(list(range(self.SPAWN_POINTS_COUNT)))
        # Update recently spawned time
        self.recently_spawned[idx] = GLOBAL_CLOCK.time
        return self.spawn_angles[idx]

    def _update_available_indexes(self):
        """
        Iterate through the recent indexes and make them available if their cooldown has expired
        """
        for idx in list(self.recently_spawned.keys()):
            if GLOBAL_CLOCK.time_since(self.recently_spawned[idx]) > self.SPAWN_COOLDOWN_SECONDS:
                self.available_indexes.add(idx)
                del self.recently_spawned[idx]
        
    def _get_enemy_spawn_position_at_random(self, player_position, window_width, window_height):
        """
        Get coordinates for an enemy spawn around the player in an arc. The steps are:
        1. Choose an angle at random, say between -20 degrees and +20 degrees (to the right of the player).
            Updated logic: choose from a discrete set of spawn angles. Also considers whether there was
            a spawn there recently.
        2. Check the edge of the screen at which to spawn - top, right or bottom
        3. Provide some offset, so that the spawn happens offscreen
        4. Return the coordinates (x, y)
        """
        angle_degrees = self._get_spawn_angle()
        x_distance_to_edge = window_width - player_position[0]
        cutoff_angle_degrees = math.degrees(math.atan2(window_height/2, x_distance_to_edge))
        if -cutoff_angle_degrees <= angle_degrees <= cutoff_angle_degrees:
            x = window_width + self.OFFSCREEN_SPAWN_OFFSET_PIXELS
            y = player_position[1] + x_distance_to_edge * math.tan(math.radians(angle_degrees))
        else:
            x = player_position[0] + (window_height / (2 * math.tan(math.radians(abs(angle_degrees)))))
            if angle_degrees > 0:
                y = window_height + self.OFFSCREEN_SPAWN_OFFSET_PIXELS
            else:
                y = -self.OFFSCREEN_SPAWN_OFFSET_PIXELS
        return x, y
    
    def spawn_enemy(self, player_position, window_width, window_height):
        enemy_word = EnemyWord(
            self.word_manager.generate_word(min_character_count=4, max_character_count=7), 
            position=self._get_enemy_spawn_position_at_random(player_position, window_width, window_height), 
            target_position=player_position
        )
        return enemy_word


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


def calculate_angle(point1, point2):
    """
    Calculate the angle (in radians, anticlockwise) of the line: (point1 -> point2)
    """
    dy = point2[1] - point1[1]
    dx = point2[0] - point1[0]
    theta = math.atan2(dy, dx)
    return theta


class WordManager:
    """Class for loading and managing words"""

    def __init__(self, file_path="words_v1.txt"):
        self._load_words(file_path)
        self._split_word_list_by_character_count()

    def _load_words(self, file_path):
        """
        Load the words from the text file.
        """
        self.word_list = []
        with open(file_path, 'r') as file:
            self.word_list = list(set(file.read().split()))
    
    def _split_word_list_by_character_count(self):
        self.character_count_dict = defaultdict(list)
        for word in self.word_list:
            self.character_count_dict[len(word)].append(word)

    def generate_word(self, min_character_count=4, max_character_count=7):
        """
        Generate new words by sampling from the existing list
        """
        character_count = random.randint(min_character_count, max_character_count)
        word = random.choice(self.character_count_dict[character_count])
        return word
    

class WelcomeView(arcade.View):

    def __init__(self):
        super().__init__()
        self.text_batch = Batch()
        self.title_text = arcade.Text(
            "Welcome to AI Typing Trainer!",
            x = self.window.width // 2,
            y = self.window.height // 2,
            anchor_x="center",
            font_size=40,
            batch=self.text_batch
        )
        self.instruction_text = arcade.Text(
            "Press ENTER to start or ESCAPE to quit", 
            x = self.title_text.x,
            y = self.title_text.y - 50,
            anchor_x="center",
            font_size=20,
            batch=self.text_batch
        )

    def on_show_view(self):
        self.window.default_camera.use()

    def on_draw(self):
        self.clear() # This is IMPORTANT! The text looks jagged without this!
        self.text_batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
        elif symbol == arcade.key.ESCAPE:
            arcade.exit()


class PauseView(arcade.View):

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.text_batch = Batch()
        self.title_text = arcade.Text(
            "Game Paused",
            x = self.window.width // 2,
            y = self.window.height // 2,
            anchor_x="center",
            font_size=40,
            batch=self.text_batch
        )
        self.score_text = arcade.Text(
            f"Your Score: {self.game_view.score}", 
            x = self.title_text.x,
            y = self.title_text.y - 50,
            anchor_x="center",
            font_size=28,
            batch=self.text_batch
        )
        self.instruction_text = arcade.Text(
            "Press ENTER to resume or ESCAPE to quit", 
            x = self.title_text.x,
            y = self.title_text.y - 100,
            anchor_x="center",
            font_size=20,
            batch=self.text_batch
        )

    def on_show_view(self):
        self.window.default_camera.use()

    def on_draw(self):
        self.clear() # This is IMPORTANT! The text looks jagged without this!
        self.text_batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            self.window.show_view(self.game_view)
        elif symbol == arcade.key.ESCAPE:
            welcome_view = WelcomeView()
            self.window.show_view(welcome_view)


class GameOverView(arcade.View):

    def __init__(self, score):
        super().__init__()
        self.score = score
        self.text_batch = Batch()
        self.title_text = arcade.Text(
            "GAME OVER!",
            x = self.window.width // 2,
            y = self.window.height // 2,
            anchor_x="center",
            font_size=40,
            batch=self.text_batch
        )
        self.score_text = arcade.Text(
            f"Your Score: {self.score}", 
            x = self.title_text.x,
            y = self.title_text.y - 50,
            anchor_x="center",
            font_size=28,
            batch=self.text_batch
        )
        self.instruction_text = arcade.Text(
            "Press any key to continue", 
            x = self.title_text.x,
            y = self.title_text.y - 100,
            anchor_x="center",
            font_size=20,
            batch=self.text_batch
        )

    def on_show_view(self):
        self.window.default_camera.use()

    def on_draw(self):
        self.clear() # This is IMPORTANT! The text looks jagged without this!
        self.text_batch.draw()

    def on_key_press(self, symbol, modifiers):
        welcome_view = WelcomeView()
        self.window.show_view(welcome_view)


def main():
    window = arcade.Window(1280, 720, "AI Typing Trainer")
    # game_view = GameView()
    # game_view.setup()
    welcome_view = WelcomeView()
    window.show_view(welcome_view)
    arcade.run()

if __name__ == "__main__":
    main()
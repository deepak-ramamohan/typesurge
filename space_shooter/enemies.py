import arcade
from arcade.clock import GLOBAL_CLOCK
import random
import math
from utils.helpers import calculate_angle_between_points
from pyglet.graphics import Batch
from utils.word_manager import WordManager
import numpy as np
from utils.colors import BROWN
from utils.resources import METEOR_SPRITE_1, METEOR_SPRITE_2


class EnemyWord(arcade.Sprite):
    """
    Requirements:
    1. Each word consists of individual characters
    2. We need to partially match the user input with the word (example: "hel" matches "hello" partially)
    3. We need to color the partially matched characters separately (e.g., in red)
    4. We need to draw and update the text characters on the screen

    """

    MATCHED_COLOR = arcade.color.ANTIQUE_BRASS
    UNMATCHED_COLOR = BROWN
    FONT_NAME = "Pixelzone"
    FONT_SIZE = 42
    # METEOR_SPRITE_OPTIONS = [
    #     ":resources:/images/space_shooter/meteorGrey_med1.png",
    #     ":resources:/images/space_shooter/meteorGrey_med2.png"
    # ]
    METEOR_SPRITE_OPTIONS = [
        METEOR_SPRITE_1,
        METEOR_SPRITE_2
    ]
    METEOR_SPRITE_SCALE = 0.35
    METEOR_SPRITE_COLOR = BROWN

    def __init__(
        self, 
        word, 
        position,
        target_position,
        movement_speed_range, 
    ):
        self.meteor_sprite_texture = random.choice(self.METEOR_SPRITE_OPTIONS)
        x, y = position
        super().__init__(
            self.meteor_sprite_texture, 
            center_x=x, 
            center_y=y,
            scale=self.METEOR_SPRITE_SCALE
        )
        self.color = self.METEOR_SPRITE_COLOR
        self.movement_speed = random.uniform(
            movement_speed_range[0],
            movement_speed_range[1]
        )
        self.change_angle = random.uniform(-5.0, 5.0)
        theta = calculate_angle_between_points(position, target_position)
        self.velocity = [
            self.movement_speed * math.cos(theta), 
            self.movement_speed * math.sin(theta)
        ]
        self.WORD_OFFSET_PIXELS = 35
        self.word = word
        self.text_characters = [c for c in word]
        self.text_batch = Batch()
        self.text_list = []
        for c in self.text_characters:
            text = arcade.Text(
                text=c, 
                x=x, 
                y=y, 
                color=self.UNMATCHED_COLOR,
                font_name=self.FONT_NAME,
                font_size=self.FONT_SIZE, 
                batch=self.text_batch, 
                anchor_y='center'
            )
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

    def __init__(self):
        super().__init__()

    def draw(self):
        for enemy_word in self:
            arcade.draw_sprite(enemy_word)
            enemy_word.text_batch.draw()


class EnemySpawner():

    ANGLE_RANGE_DEGREES = 45
    OFFSCREEN_SPAWN_OFFSET_PIXELS = 30
    SPAWN_POINTS_COUNT = 9  # Number of distinct spawn points
    SPAWN_COOLDOWN_SECONDS = 5

    def __init__(self):
        self.word_manager = WordManager()
        self.spawn_angles = np.linspace(
            -self.ANGLE_RANGE_DEGREES/2, 
            self.ANGLE_RANGE_DEGREES/2,
            self.SPAWN_POINTS_COUNT
        )
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
    
    def spawn_enemy_word(
        self, 
        player_position, 
        window_width, 
        window_height,
        character_count_range=[4, 7],
        movement_speed_range=[0.75, 1.25]
    ):
        enemy_word = EnemyWord(
            self.word_manager.generate_word(
                min_character_count=character_count_range[0],
                max_character_count=character_count_range[1]
            ), 
            position=self._get_enemy_spawn_position_at_random(
                player_position, 
                window_width, 
                window_height
            ), 
            target_position=player_position,
            movement_speed_range=movement_speed_range
        )
        return enemy_word

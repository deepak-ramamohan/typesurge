import arcade
import random
import math
from space_shooter.player import Player
from space_shooter.enemies import EnemySpawner, EnemyWordList
from space_shooter.explosion import Explosion
from utils.helpers import calculate_angle_between_points, key_mapping
from pyglet.graphics import Batch
from arcade.gui import (
    UIManager,
    UIAnchorLayout,
    UIBoxLayout, 
    UIFlatButton
)


class SpaceShooterGameView(arcade.View):

    BACKGROUND_COLOR = arcade.color.CHARCOAL
    ENEMY_COUNT_RANGE = [2, 5]
    ENEMY_WORD_CHARACTER_COUNT_RANGE = [4, 7]
    ENEMY_MOVEMENT_SPEED_RANGE = [0.75, 1.25]
    LASER_SPEED = 40
    SOUND_VOLUME = 1.0
    FONT_NAME = "Pixelzone"
    
    def __init__(self, main_menu_view):
        super().__init__(background_color=self.BACKGROUND_COLOR)
        self.main_menu_view = main_menu_view
        self.enemy_spawner = EnemySpawner()
        self.player = Player(center_x=75, center_y=self.height//2)
        self.player_lives_text = arcade.Text(
            text="", 
            x=10, 
            y=15, 
            font_name=self.FONT_NAME,
            font_size=32, 
            bold=True
        )
        self.input = ""
        self.explosion_list = None
        self.score = 0
        self.score_text = arcade.Text(
            text="",
            x=10,
            y=50,
            font_name=self.FONT_NAME,
            font_size=32,
            bold=True
        )
        self._load_explosion_texture_list()
        self.laser_sound = arcade.Sound(":resources:/sounds/laser2.wav")
        self.explosion_sound = arcade.Sound(":resources:/sounds/explosion2.wav")
        self.game_over_sound = arcade.Sound(":resources:/sounds/gameover3.wav")
        # For fixing the initial sound distortion, play something at zero volume
        # Subsequent sounds will then play clearly
        arcade.play_sound(self.laser_sound, volume=0)

    def setup(self):
        self.input = ""
        self.player.reset_lives()
        self._update_player_lives_text()
        self.score = 0
        self._update_score_text()
        self.laser_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()
        self.enemy_word_list = EnemyWordList()
        self._spawn_enemies()

    def on_draw(self):
        self.clear()
        self.laser_list.draw()
        arcade.draw_sprite(self.player)
        self.enemy_word_list.draw()
        self.explosion_list.draw()
        self.score_text.draw()
        self.player_lives_text.draw()

    def _spawn_enemies(self):
        """
        Keep spawning enemies to ensure that the count is between ENEMY_COUNT_MIN and ENEMY_COUNT_MAX
        """
        current_enemy_count = len(self.enemy_word_list)
        count_target = random.randrange(
            self.ENEMY_COUNT_RANGE[0], 
            self.ENEMY_COUNT_RANGE[1] + 1
        )
        while current_enemy_count < count_target:
            enemy_word = self.enemy_spawner.spawn_enemy_word(
                player_position=self.player.position,
                window_width=self.width,
                window_height=self.height,
                character_count_range=self.ENEMY_WORD_CHARACTER_COUNT_RANGE,
                movement_speed_range=self.ENEMY_MOVEMENT_SPEED_RANGE
            )
            self.enemy_word_list.append(enemy_word)
            current_enemy_count += 1

    def _reset_difficulty(self):
        self.ENEMY_COUNT_RANGE = [2, 5]
        self.ENEMY_WORD_CHARACTER_COUNT_RANGE = [4, 7]
        self.ENEMY_MOVEMENT_SPEED_RANGE = [0.75, 1.25]

    def _update_difficulty(self):
        if self.score < 500:
            pass
        elif self.score < 1000:
            self.ENEMY_MOVEMENT_SPEED_RANGE[0] = 0.8
        elif self.score < 1500:
            self.ENEMY_COUNT_RANGE[0] = 3
        elif self.score < 2000:
            self.ENEMY_MOVEMENT_SPEED_RANGE[0] = 0.85
        elif self.score < 3000:
            self.ENEMY_WORD_CHARACTER_COUNT_RANGE[0] = 5
        elif self.score < 4000:
            self.ENEMY_MOVEMENT_SPEED_RANGE[1] = 1.35
        elif self.score < 5000:
            self.ENEMY_COUNT_RANGE[1] = 6
        elif self.score < 6500:
            self.ENEMY_MOVEMENT_SPEED_RANGE[0] = 0.9
        elif self.score < 8000:
            self.ENEMY_WORD_CHARACTER_COUNT_RANGE[1] = 8
        elif self.score < 10000:
            self.ENEMY_COUNT_RANGE[0] = 4
        elif self.score < 12000:
            self.ENEMY_WORD_CHARACTER_COUNT_RANGE[1] = 9
        elif self.score < 14000:
            self.ENEMY_MOVEMENT_SPEED_RANGE[0] = 1.0
        elif self.score < 15000:
            self.ENEMY_MOVEMENT_SPEED_RANGE[1] = 1.5
        elif self.score < 17000:
            self.ENEMY_COUNT_RANGE[1] = 7
        elif self.score < 18500:
            self.ENEMY_WORD_CHARACTER_COUNT_RANGE[0] = 6
        elif self.score < 20000:
            self.ENEMY_WORD_CHARACTER_COUNT_RANGE[1] = 11
        elif self.score < 22500:
            self.ENEMY_MOVEMENT_SPEED_RANGE[1] = 1.65
        elif self.score < 25000:
            self.ENEMY_COUNT_RANGE[0] = 5
        elif self.score < 27500:
            self.ENEMY_MOVEMENT_SPEED_RANGE[0] = 1.2
        else:
            self.ENEMY_MOVEMENT_SPEED_RANGE[1] = 2.0
            self.ENEMY_COUNT_RANGE[1] = 9
            self.ENEMY_WORD_CHARACTER_COUNT_RANGE[1] = 13
        

    def _fire_laser_at(self, enemy_word):
        laser = arcade.Sprite(":resources:/images/space_shooter/laserBlue01.png")
        laser.center_y = self.player.center_y
        laser.left = self.player.right
        theta = calculate_angle_between_points(laser.position, enemy_word.position)
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
                self._spawn_enemies()
                self._update_difficulty()

    def _check_player_collision(self):
        collisions = arcade.check_for_collision_with_list(self.player, self.enemy_word_list)
        if collisions:
            self._create_explosions_at_sprites(collisions)
            self.player.lives_remaining -= 1
            self._update_player_lives_text()
            self._spawn_enemies()
            if self.player.lives_remaining <= 0:
                game_over_view = GameOverView(self.score, self.main_menu_view)
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

    def _update_score_text(self):
        self.score_text.text = f"Score: {self.score}"

    def _update_player_lives_text(self):
        self.player_lives_text.text = f"Lives: {self.player.lives_remaining}/{self.player.MAX_LIVES}"
            
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)
        key_pressed = key_mapping.get(symbol, "")
        self.input = self.input + key_pressed


class PauseView(arcade.View):

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.text_batch = Batch()
        self.title_text = arcade.Text(
            "Game Paused",
            x = self.window.width // 2,
            y = self.window.height // 2 + 150,
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
        self.ui = UIManager()
        self.anchor = self.ui.add(UIAnchorLayout())
        self.BUTTON_WIDTH = 200

        self.resume_button = UIFlatButton(width=self.BUTTON_WIDTH, text="Resume")
        @self.resume_button.event("on_click")
        def _(event):
            self._resume()

        self.quit_to_main_menu_button = UIFlatButton(width=self.BUTTON_WIDTH, text="Quit to Main Menu", multiline=True)
        @self.quit_to_main_menu_button.event("on_click")
        def _(event):
            self._return_to_main_menu()

        self.box_layout = UIBoxLayout(space_between=10)
        self.box_layout.add(self.resume_button)
        self.box_layout.add(self.quit_to_main_menu_button)
        self.anchor.add(
            self.box_layout,
            anchor_y="top",
            align_y=-(self.height - self.title_text.y + 120)
        )

    def on_show_view(self):
        self.window.default_camera.use()
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_draw(self):
        self.clear() # This is IMPORTANT! The text looks jagged without this!
        self.text_batch.draw()
        self.ui.draw()

    def _resume(self):
        self.window.show_view(self.game_view)

    def _return_to_main_menu(self):
        self.window.show_view(self.game_view.main_menu_view)


class GameOverView(arcade.View):

    def __init__(self, score, main_menu_view):
        super().__init__()
        self.score = score
        self.main_menu_view = main_menu_view
        self.text_batch = Batch()
        self.title_text = arcade.Text(
            "GAME OVER!",
            x = self.window.width // 2,
            y = self.window.height // 2 + 50,
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

        self.ui = UIManager()
        self.anchor = self.ui.add(UIAnchorLayout())
        self.BUTTON_WIDTH = 200

        self.continue_button = UIFlatButton(width=self.BUTTON_WIDTH, text="Continue")
        @self.continue_button.event("on_click")
        def _(event):
            self._continue_to_main_menu()

        self.box_layout = UIBoxLayout(space_between=10)
        self.box_layout.add(self.continue_button)
        self.anchor.add(
            self.box_layout,
            anchor_y="top",
            align_y=-(self.height - self.title_text.y + 110)
        )

    def on_show_view(self):
        self.window.default_camera.use()
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_draw(self):
        self.clear() # This is IMPORTANT! The text looks jagged without this!
        self.text_batch.draw()
        self.ui.draw()

    def _continue_to_main_menu(self):
        self.window.show_view(self.main_menu_view)

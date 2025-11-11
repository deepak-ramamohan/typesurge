import arcade
from arcade.gui import UIOnClickEvent
import random
import math
from space_shooter.player import Player
from space_shooter.enemies import EnemySpawner, EnemyWordList, EnemyWord
from space_shooter.explosion import Explosion
from utils.helpers import calculate_angle_between_points, key_mapping
from utils.resources import (
    SEPIA_BACKGROUND, 
    BULLET_SPRITE, 
    SPACE_SHOOTER_MUSIC, 
    KEYPRESS_SOUND, 
    ERROR_SOUND,
    GAME_OVER_SOUND
)
from utils.menu_view import MenuView
from utils.colors import BROWN
from utils.music_manager import MusicManager


class SpaceShooterGameView(arcade.View):
    """
    The main game view.
    """

    BACKGROUND_COLOR = arcade.color.CHARCOAL
    ENEMY_COUNT_RANGE = [2, 5]
    ENEMY_WORD_CHARACTER_COUNT_RANGE = [4, 7]
    ENEMY_MOVEMENT_SPEED_RANGE = [0.75, 1.25]
    LASER_SPEED = 40
    SOUND_VOLUME = 1.0
    FONT_NAME = "Pixelzone"
    
    def __init__(self, main_menu_view: arcade.View) -> None:
        """
        Initializer
        """
        super().__init__(background_color=self.BACKGROUND_COLOR)
        self.window.set_mouse_visible(False)
        self.main_menu_view = main_menu_view
        self.enemy_spawner = EnemySpawner()
        self.player = Player(center_x=75, center_y=self.window.height//2)
        self.player_lives_text = arcade.Text(
            text="", 
            x=10, 
            y=15, 
            font_name=self.FONT_NAME,
            font_size=32,
            color=arcade.color.ANTIQUE_RUBY,
            bold=True
        )
        self.input = ""
        self.explosion_list: arcade.SpriteList
        self.score = 0
        self.score_text = arcade.Text(
            text="",
            x=10,
            y=50,
            font_name=self.FONT_NAME,
            font_size=32,
            color=arcade.color.ANTIQUE_RUBY,
            bold=True
        )
        self.multiplier = 1.0
        self.streak = 0
        self._load_explosion_texture_list()
        self.laser_sound = arcade.Sound(":resources:/sounds/laser2.wav")
        self.explosion_sound = arcade.Sound(":resources:/sounds/explosion2.wav")
        self.game_over_sound = arcade.Sound(":resources:/sounds/gameover3.wav")
        # For fixing the initial sound distortion, play something at zero volume
        # Subsequent sounds will then play clearly
        arcade.play_sound(self.laser_sound, volume=0)
        MusicManager.play_music(SPACE_SHOOTER_MUSIC)
        self.setup()

    def setup(self) -> None:
        """
        Set up the game.
        """
        self.input = ""
        self.player.reset_lives()
        self._update_player_lives_text()
        self.score = 0
        self._update_score_text()
        self.laser_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()
        self.enemy_word_list = EnemyWordList()
        self._spawn_enemies()

    def on_draw(self) -> None:
        """
        Draw the game.
        """
        self.clear()
        arcade.draw_texture_rect(
            SEPIA_BACKGROUND,
            arcade.LBWH(0, 0, self.window.width, self.window.height)
        )
        self.laser_list.draw()
        arcade.draw_sprite(self.player)
        self.enemy_word_list.draw()
        self.explosion_list.draw()
        self.score_text.draw()
        self.player_lives_text.draw()

    def _spawn_enemies(self) -> None:
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
                window_width=self.window.width,
                window_height=self.window.height,
                character_count_range=self.ENEMY_WORD_CHARACTER_COUNT_RANGE,
                movement_speed_range=self.ENEMY_MOVEMENT_SPEED_RANGE
            )
            self.enemy_word_list.append(enemy_word)
            current_enemy_count += 1

    def _reset_difficulty(self) -> None:
        """
        Reset the difficulty.
        """
        self.ENEMY_COUNT_RANGE = [2, 5]
        self.ENEMY_WORD_CHARACTER_COUNT_RANGE = [4, 7]
        self.ENEMY_MOVEMENT_SPEED_RANGE = [0.75, 1.25]

    def _update_difficulty(self) -> None:
        """
        Update the difficulty based on the score.
        """
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
        

    def _fire_laser_at(self, enemy_word: "EnemyWord") -> None:
        """
        Fire a laser at the given enemy word.
        """
        # laser = arcade.Sprite(":resources:/images/space_shooter/laserRed01.png")
        laser = arcade.Sprite(BULLET_SPRITE, scale=0.2)
        laser.color = BROWN
        LASER_ANGLE_OFFSET = 90
        laser.center_y = self.player.center_y
        laser.left = self.player.right
        theta = calculate_angle_between_points(laser.position, enemy_word.position)
        laser.velocity = (self.LASER_SPEED * math.cos(theta), self.LASER_SPEED * math.sin(theta))
        laser.angle = math.degrees(2 * math.pi - theta) + LASER_ANGLE_OFFSET
        self.laser_list.append(laser)
        arcade.play_sound(self.laser_sound, volume=self.SOUND_VOLUME)

    def _load_explosion_texture_list(self) -> None:
        """
        Load the explosion texture list.
        """
        spritesheet = arcade.load_spritesheet(":resources:images/spritesheets/explosion.png")
        self.explosion_texture_list = spritesheet.get_texture_grid(
            size=(256, 256),
            columns=16,
            count=16*10
        )

    def _create_explosions_at_sprites(self, sprites_list: list[arcade.Sprite]) -> None:
        """
        Create explosions at the given sprites.
        """
        for sprite in sprites_list:
            arcade.play_sound(self.explosion_sound, volume=self.SOUND_VOLUME)
            explosion = Explosion(self.explosion_texture_list)
            explosion.position = sprite.position
            self.explosion_list.append(explosion)
            sprite.remove_from_sprite_lists()

    def _add_scores_from_words(self, enemy_words: list["EnemyWord"]) -> None:
        """
        Add scores from the given enemy words.
        """
        for enemy_word in enemy_words:
            self.score += 20 * self.multiplier * len(enemy_word.word)
        self._update_score_text()

    def _check_laser_collisions(self, delta_time: float) -> None:
        """
        Check for laser collisions.
        """
        self.laser_list.update()
        for laser in self.laser_list:
            if laser.left > self.window.width:
                laser.remove_from_sprite_lists()
            collisions = arcade.check_for_collision_with_list(laser, self.enemy_word_list)
            if collisions:
                laser.remove_from_sprite_lists()
                self._add_scores_from_words(collisions)
                self._create_explosions_at_sprites(collisions)
                self._spawn_enemies()
                self._update_difficulty()

    def _check_player_collision(self) -> None:
        """
        Check for player collision.
        """
        collisions = arcade.check_for_collision_with_list(self.player, self.enemy_word_list)
        if collisions:
            self._create_explosions_at_sprites(collisions)
            self.player.lives_remaining -= 1
            self._update_player_lives_text()
            self._spawn_enemies()
            if self.player.lives_remaining <= 0:
                game_over_view = GameOverView(int(self.score), self.main_menu_view)
                arcade.play_sound(GAME_OVER_SOUND, volume=1.0)
                self.window.show_view(game_over_view)

    def _check_word_matches(self) -> None:
        """
        Check for word matches.
        """
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
        if mismatch_count == len(self.enemy_word_list):
            self.input = ""
            self._play_error_sound()
            self.streak = 0
        elif full_match_count > 0:
            self.input = ""
            self._play_keypress_sound()
            self.streak += 1
        else:
            self._play_keypress_sound()
        self._update_multiplier()

    def on_update(self, delta_time: float) -> None:
        """
        Update the game.
        """
        self._check_player_collision()
        self._check_laser_collisions(delta_time=delta_time)
        self.explosion_list.update(delta_time=delta_time)
        self.enemy_word_list.update(delta_time=delta_time)
        # self._check_word_matches()

    def _update_multiplier(self) -> None:
        self.multiplier = min(1.0 + self.streak / 10.0, 5.0)
        self._update_score_text()

    def _update_score_text(self) -> None:
        """
        Update the score text.
        """
        self.score_text.text = f"Score: {self.score:.0f}, Multiplier: {self.multiplier:.1f}x"

    def _update_player_lives_text(self) -> None:
        """
        Update the player lives text.
        """
        self.player_lives_text.text = f"Lives: {self.player.lives_remaining}/{self.player.MAX_LIVES}"
            
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """
        Handle key presses.
        """
        if symbol == arcade.key.ESCAPE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)
        else:
            key_pressed = key_mapping.get(symbol, "")
            self.input = self.input + key_pressed
            self._check_word_matches()

    def _play_keypress_sound(self):
        """
        Play the keypress sound
        """
        arcade.play_sound(
            KEYPRESS_SOUND, 
            volume=random.uniform(0.55, 0.65),
            speed=random.uniform(0.98, 1.02)
        )

    def _play_error_sound(self):
        arcade.play_sound(ERROR_SOUND, volume=0.4)

    def on_show_view(self) -> None:
        """
        Handle show view.
        """
        self.window.set_mouse_visible(False)

    def on_hide_view(self) -> None:
        """
        Handle hide view.
        """
        self.window.set_mouse_visible(True)


class PauseView(MenuView):
    """
    The pause view.
    """

    def __init__(self, game_view: SpaceShooterGameView) -> None:
        """
        Initializer
        """
        self.game_view = game_view
        title_text = "Game Paused"
        subtitle_text = f"Your Score: {self.game_view.score}"
        self.TITLE_FONT_SIZE = 64
        super().__init__(
            title_text=title_text,
            subtitle_text=subtitle_text
        )

        resume_button = self.create_button("Resume")
        @resume_button.event("on_click")
        def _(event: "UIOnClickEvent") -> None:
            """
            Resume the game.
            """
            self._resume()

        quit_to_main_menu_button = self.create_button("Quit to Main Menu")
        @quit_to_main_menu_button.event("on_click")
        def _(event: "UIOnClickEvent") -> None:
            """
            Return to the main menu.
            """
            self._return_to_main_menu()

        self.initialize_buttons(
            [
                resume_button,
                quit_to_main_menu_button
            ]
        )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """
        Handle key presses.
        """
        if symbol == arcade.key.ESCAPE:
            self._resume()

    def _resume(self) -> None:
        """
        Resume the game.
        """
        self.window.show_view(self.game_view)

    def _return_to_main_menu(self) -> None:
        """
        Return to the main menu.
        """
        self.window.show_view(self.game_view.main_menu_view)


class GameOverView(MenuView):
    """
    The game over view.
    """

    def __init__(self, score: int, main_menu_view: arcade.View) -> None:
        """
        Initializer
        """
        self.score = score
        self.main_menu_view = main_menu_view
        score_text = f"Your Score: {self.score}"
        super().__init__(
            title_text="Game Over!",
            subtitle_text=score_text
        )

        continue_button = self.create_button("Continue")
        @continue_button.event("on_click")
        def _(event: "UIOnClickEvent") -> None:
            """
            Continue to the main menu.
            """
            self._continue_to_main_menu()

        self.initialize_buttons(
            [
                continue_button
            ]
        )

    def _continue_to_main_menu(self) -> None:
        """
        Continue to the main menu.
        """
        self.window.show_view(self.main_menu_view)

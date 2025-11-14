import arcade
from arcade.gui import UIOnClickEvent
import random
import math
from space_shooter.player import Player
from space_shooter.enemies import EnemySpawner, EnemyWordList, EnemyWord
from space_shooter.explosion import Explosion
from space_shooter.laser import Laser
from space_shooter.game_stats import GameStats
from space_shooter.difficulty import Difficulty
from utils.helpers import key_mapping
from utils.resources import (
    SEPIA_BACKGROUND,
    SPACE_SHOOTER_MUSIC, 
    KEYPRESS_SOUND, 
    ERROR_SOUND,
    GAME_OVER_SOUND
)
from utils.menu_view import MenuView
from utils.music_manager import MusicManager
from utils import global_state
from utils.save_manager import SaveManager


class SpaceShooterGameView(arcade.View):
    """
    The main game view.
    """

    SOUND_VOLUME = 1.0
    FONT_NAME = "Pixelzone"
    
    def __init__(self, main_menu_view: arcade.View, difficulty_level: int = 1) -> None:
        """
        Initializer
        """
        super().__init__()
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
        self.game_stats = GameStats()
        self.game_stats.score = 0
        self.score_text = arcade.Text(
            text="",
            x=10,
            y=50,
            font_name=self.FONT_NAME,
            font_size=32,
            color=arcade.color.ANTIQUE_RUBY,
            bold=True
        )
        self.difficulty = Difficulty(difficulty_level=difficulty_level)
        self.multiplier = 1.0
        self.streak = 0
        self._load_explosion_texture_list()
        self.explosion_sound = arcade.Sound(":resources:/sounds/explosion2.wav")
        self.game_over_sound = arcade.Sound(":resources:/sounds/gameover3.wav")
        MusicManager.play_music(SPACE_SHOOTER_MUSIC)
        self.setup()

    def setup(self) -> None:
        """
        Set up the game.
        """
        self.input = ""
        self._update_player_lives_text()
        self.game_stats.score = 0
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
        self.player.draw()
        self.enemy_word_list.draw()
        self.explosion_list.draw()
        self.score_text.draw()
        self.player_lives_text.draw()

    def _spawn_enemies(self) -> None:
        """
        Keep spawning enemies according to the difficulty setting
        """
        current_enemy_count = len(self.enemy_word_list)
        count_target = random.randrange(
            self.difficulty.enemy_count.min, 
            self.difficulty.enemy_count.max + 1
        )
        while current_enemy_count < count_target:
            enemy_word = self.enemy_spawner.spawn_enemy_word(
                player_position=self.player.position,
                window_width=self.window.width,
                window_height=self.window.height,
                character_count_range=[
                    self.difficulty.enemy_word_length.min,
                    self.difficulty.enemy_word_length.max
                ],
                movement_speed_range=[
                    self.difficulty.enemy_movement_speed.min,
                    self.difficulty.enemy_movement_speed.max
                ]
            )
            self.enemy_word_list.append(enemy_word)
            current_enemy_count += 1

    def _update_difficulty(self) -> None:
        """
        Update the difficulty based on the score.
        """
        self.difficulty.update_difficulty(self.game_stats.score)
        
    def _fire_laser_at(self, enemy_word: EnemyWord) -> None:
        """
        Fire a laser at the given enemy word.
        """
        laser = Laser(self.player, enemy_word)
        self.laser_list.append(laser)

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

    def _create_explosion_at_sprite(self, sprite: arcade.Sprite) -> None:
        """
        Create an explosion at the given sprite (and remove the sprite).
        """
        arcade.play_sound(self.explosion_sound, volume=self.SOUND_VOLUME)
        explosion = Explosion(self.explosion_texture_list)
        explosion.position = sprite.position
        self.explosion_list.append(explosion)
        sprite.remove_from_sprite_lists()

    def _add_score_from_word(self, enemy_word: EnemyWord) -> None:
        """
        Add scores from the given enemy words.
        """
        self.game_stats.score += int(20 * self.multiplier * len(enemy_word.word))
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
            for enemy_word in collisions:
                if enemy_word == laser.target:
                    laser.remove_from_sprite_lists()
                    self._add_score_from_word(enemy_word)
                    self._create_explosion_at_sprite(enemy_word)
                    self._spawn_enemies()
                    self._update_difficulty()

    def _check_player_collision(self) -> None:
        """
        Check if any of the enemy words collides with the player.
        Update player lives and show 'Game Over' if no lives remain.
        """
        collisions = arcade.check_for_collision_with_list(self.player, self.enemy_word_list)
        for enemy_word in collisions:
            self._create_explosion_at_sprite(enemy_word)
            self.player.lives_remaining -= 1
            self._update_player_lives_text()
            self._spawn_enemies()
            if self.player.lives_remaining <= 0:
                game_over_view = GameOverView(self.game_stats, self.main_menu_view)
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

    def _update_multiplier(self) -> None:
        multiplier = min(
            1.0 + self.streak * 1.0 / self.difficulty.difficulty_setting.multiplier_streak, 
            self.difficulty.difficulty_setting.multiplier_limit
        )
        self.multiplier = math.floor(multiplier)
        self._update_score_text()

    def _update_score_text(self) -> None:
        """
        Update the score text.
        """
        self.score_text.text = f"Score: {self.game_stats.score:.0f}, Multiplier: {self.multiplier:.0f}x"

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
            pause_view = PauseView(self, self.game_stats)
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


class SSDifficultySelectionView(MenuView):
    """View for choosing Space Shooter's difficulty"""

    def __init__(self, previous_view: arcade.View, main_menu_view: arcade.View) -> None:
        super().__init__(
            title_text="Space Shooter",
            subtitle_text="Choose your difficulty", 
            previous_view=previous_view
        )
        self.main_menu_view = main_menu_view

        button_easy = self.create_button(
            button_text="Easy",
            tooltip_text="Fewer meteors with shorter words. Recommended for beginners."
        )
        @button_easy.event("on_click")
        def _(event: UIOnClickEvent) -> None:
            self._start_game(0)

        button_moderate = self.create_button(
            button_text="Moderate",
            tooltip_text="More meteors with longer words. Recommended for fast typists."
        )
        @button_moderate.event("on_click")
        def _(event: UIOnClickEvent) -> None:
            self._start_game(1)

        button_hard = self.create_button(
            button_text="Hard",
            tooltip_text="Even more meteors with much longer words. A real challenge."
        )
        @button_hard.event("on_click")
        def _(event: UIOnClickEvent) -> None:
            self._start_game(2)

        button_back = self.create_button(
            button_text="Back",
            tooltip_text="Return to the Main Menu"
        )
        @button_back.event("on_click")
        def _(event: UIOnClickEvent) -> None:
            self.return_to_previous_view()

        self.initialize_buttons(
            [
                button_easy,
                button_moderate,
                button_hard,
                button_back
            ]
        )
    
    def _start_game(self, difficulty_level: int) -> None:
        """
        Start the Space Shooter game with the chosen difficulty
        """
        game_view = SpaceShooterGameView(self.main_menu_view, difficulty_level=difficulty_level)
        self.window.show_view(game_view)


class PauseView(MenuView):
    """
    The pause view.
    """

    def __init__(self, game_view: SpaceShooterGameView, game_stats: GameStats) -> None:
        """
        Initializer
        """
        self.game_view = game_view
        self.game_stats = game_stats
        self.save_manager = SaveManager(global_state.current_user_profile)
        title_text = "Game Paused"
        subtitle_text = f"Your Score: {self.game_view.game_stats.score}"
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
        self.save_manager.save_game_score_to_db(self.game_stats)
        self.window.show_view(self.game_view.main_menu_view)


class GameOverView(MenuView):
    """
    The game over view.
    """

    def __init__(self, game_stats: GameStats, main_menu_view: arcade.View) -> None:
        """
        Initializer
        """
        self.save_manager = SaveManager(global_state.current_user_profile)
        self.save_manager.save_game_score_to_db(game_stats)
        high_score = self.save_manager.get_all_game_stats().get_high_score()
        self.main_menu_view = main_menu_view
        if game_stats.score == high_score:
            score_text = f"Your Score: {game_stats.score}\nNew High Score!"
        else:
            score_text = f"Your Score: {game_stats.score}\nYour High Score: {high_score}"
        super().__init__(
            title_text="Game Over!",
            subtitle_text=score_text
        )

        restart_button = self.create_button("Restart")
        @restart_button.event("on_click")
        def _(event: UIOnClickEvent) -> None:
            self._restart_game()

        return_to_main_menu_button = self.create_button("Return to Main Menu")
        @return_to_main_menu_button.event("on_click")
        def _(event: "UIOnClickEvent") -> None:
            """
            Return to the main menu.
            """
            self._return_to_main_menu()

        self.initialize_buttons(
            [
                restart_button,
                return_to_main_menu_button
            ]
        )

    def _return_to_main_menu(self) -> None:
        """
        Continue to the main menu.
        """
        self.window.show_view(self.main_menu_view)

    def _restart_game(self) -> None:
        """
        Starts a new session of the space shooter game
        """
        game_view = SSDifficultySelectionView(self.main_menu_view, self.main_menu_view)
        self.window.show_view(game_view)

import arcade

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Arcade Tutorial - Platformer"
TILE_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
COIN_SCALING = 0.5

class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class to set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.background_color = arcade.csscolor.ANTIQUE_WHITE
        self.tile_map = None
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None
        self.camera = None
        self.can_double_jump = True
        self.score_text = None
        self.score = 0
        self.gui_camera = None
        self.coin_collected_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump3.wav")
        self.gameover_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.end_of_map = 0
        self.level = 1
        self.reset_score = True

    def _create_player_sprite(self):
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png")
        self.player_sprite.position = [128, 128]
        self.scene.add_sprite("Player", self.player_sprite)

    def _build_wall(self):
        # Using spatial hash makes collision detection faster, at the cost of slow movement
        # This is okay for stationary objects such as grass
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        for x in range(32, WINDOW_WIDTH + 1 - 32, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=TILE_SCALING)
            wall.position = [x, 32]
            self.scene.add_sprite("Walls", wall)
        for coordinate in [[512, 96], [256, 96], [768, 96]]:
            box = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", scale=TILE_SCALING)
            box.position = coordinate
            self.scene.add_sprite("Walls", box)

    def _add_coins(self):
        self.scene.add_sprite_list("Coins", use_spatial_hash=True)
        coordinates = [[256, 384], [512, 512], [768, 384]]
        for coordinate in coordinates:
            coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=COIN_SCALING)
            coin.position = coordinate
            self.scene.add_sprite("Coins", coin)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.scene = arcade.Scene()
        
        # self._build_wall()
        # self._add_coins()

        layer_options = {
            "Platforms": {
                "use_spatial_hash": True
            }
        }
        self.tile_map = arcade.load_tilemap(
            f":resources:tiled_maps/map2_level_{self.level}.json",
            scaling=TILE_SCALING,
            layer_options = layer_options
        )
        self.end_of_map = (self.tile_map.width * self.tile_map.tile_width) * self.tile_map.scaling
        print(self.end_of_map)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list_after("Player", "Foreground")
        self._create_player_sprite()

        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()
        if self.reset_score:
            self.score = 0
        self.score_text = arcade.Text(f"Score = {self.score}", 0, 5, color=(100, 100, 100), font_size=18, bold=True)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.scene["Platforms"], gravity_constant=GRAVITY
        )

    def on_draw(self):
        """Render the screen."""

        # The clear method should always be called at the start of on_draw.
        # It clears the whole screen to whatever the background color is
        # set to. This ensures that you have a clean slate for drawing each
        # frame of the game.
        self.clear()

        # Code to draw other things will go here
        self.camera.use()
        self.scene.draw()
        # Use the GUI camera to draw on the screen space
        self.gui_camera.use()
        self.score_text.draw()

    def on_update(self, delta_time):
        """Movement and game logic"""
        self.physics_engine.update()
        self._check_coin_collision()
        self._check_lava()
        self._check_end_of_level()
        self.camera.position = self.player_sprite.position

    def _check_coin_collision(self):
        coins_collected = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Coins"])
        for coin in coins_collected:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.coin_collected_sound)
            self.score += 75
            self.score_text.text = f"Score = {self.score}"

    def _check_lava(self):
        if arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Don't Touch"]
        ):
            arcade.play_sound(self.gameover_sound)
            self.setup()

    def _check_end_of_level(self):
        if self.player_sprite.center_x >= self.end_of_map:
            self.level += 1
            self.reset_score = False
            if self.level > 2:
                self.score = 0
                self.level = 1
                self.reset_score = True
            self.setup()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed"""
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.can_double_jump = True
                arcade.play_sound(self.jump_sound)
            elif self.can_double_jump:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.can_double_jump = False
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.ESCAPE:
            self.setup()

    def on_key_release(self, key, modifiers):
        """Called whenever a key is released."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
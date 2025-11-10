import arcade
from utils.colors import BROWN
from utils.helpers import load_image


# Textures
SEPIA_BACKGROUND = arcade.load_texture("assets/sepia_background.png")
METEOR_SPRITE_1 = arcade.Texture(load_image("assets/sprites/asteroid.png"))
METEOR_SPRITE_2 = arcade.Texture(load_image("assets/sprites/meteor.png"))
SPACESHIP_SPRITE = arcade.Texture(load_image("assets/sprites/spaceship_2.png"))
BULLET_SPRITE = arcade.Texture(load_image("assets/sprites/bullet.png"))
USER_PROFILE_SPRITE = arcade.Texture(
    load_image("assets/sprites/account.png", tint_color=BROWN[:3])
)

# Music
MAIN_MENU_MUSIC = arcade.Sound("assets/sounds/hard_boiled.mp3", streaming=True)
AI_TRAINER_MUSIC = arcade.Sound("assets/sounds/vibing_over_venus.mp3", streaming=True)
SPACE_SHOOTER_MUSIC = arcade.Sound("assets/sounds/space_jazz.mp3", streaming=True)

# Sounds
KEYPRESS_SOUND = arcade.Sound("assets/sounds/eklee-KeyPressMac06.wav", streaming=False)
ERROR_SOUND = arcade.Sound("assets/sounds/error-03-125761.mp3", streaming=False)
GAME_OVER_SOUND = arcade.Sound("assets/sounds/game-over-417465.mp3", streaming=False)
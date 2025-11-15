import arcade
from utils.colors import BROWN, BEIGE
from utils.helpers import load_image


# Textures
SEPIA_BACKGROUND = arcade.load_texture("assets/images/sepia_background.png")
METEOR_SPRITE_1 = arcade.load_texture("assets/sprites/meteorBrown_big1.png")
METEOR_SPRITE_2 = arcade.load_texture("assets/sprites/meteorBrown_big3.png")
METEOR_SPRITE_3 = arcade.load_texture("assets/sprites/meteorBrown_big4.png")
SPACESHIP_SPRITE = arcade.Texture(
    load_image(
        "assets/sprites/playerShip2_red.png",
        tint_color=BEIGE[:3]
    )
)
SPACESHIP_DAMAGE_SPRITE_1 = arcade.load_texture("assets/sprites/playerShip2_damage1.png")
SPACESHIP_DAMAGE_SPRITE_2 = arcade.load_texture("assets/sprites/playerShip2_damage2.png")
LASER_SPRITE = arcade.Texture(
    load_image(
        "assets/sprites/laserRed16.png",
        tint_color=BEIGE[:3]
    )
)
USER_PROFILE_SPRITE = arcade.Texture(
    load_image(
        "assets/sprites/account.png",
        invert=True,
        tint_color=BROWN[:3]
    )
)

# Texture list for explosion
EXPLOSION_SPRITESHEET = arcade.load_spritesheet("assets/images/explosion.png")
EXPLOSION_TEXTURE_LIST = EXPLOSION_SPRITESHEET.get_texture_grid(
    size=(256, 256),
    columns=16,
    count=16*10
)

# Music
MAIN_MENU_MUSIC = arcade.Sound("assets/sounds/hard_boiled.mp3", streaming=True)
AI_TRAINER_MUSIC = arcade.Sound("assets/sounds/vibing_over_venus.mp3", streaming=True)
SPACE_SHOOTER_MUSIC = arcade.Sound("assets/sounds/space_jazz.mp3", streaming=True)

# Sounds
KEYPRESS_SOUND = arcade.Sound("assets/sounds/eklee-KeyPressMac06.wav", streaming=False)
ERROR_SOUND = arcade.Sound("assets/sounds/error-03-125761.mp3", streaming=False)
GAME_OVER_SOUND = arcade.Sound("assets/sounds/game-over-417465.mp3", streaming=False)
LASER_SOUND = arcade.Sound("assets/sounds/laser2.wav", streaming=False)
EXPLOSION_SOUND = arcade.Sound("assets/sounds/explosion2.wav", streaming=False)

# Hack: for fixing the initial sound distortion, play something at zero volume
arcade.play_sound(LASER_SOUND, volume=0)
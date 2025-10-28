import arcade
from PIL import Image, ImageOps
from utils.colors import BROWN
from utils.helpers import tint_image


SEPIA_BACKGROUND = arcade.load_texture("assets/sepia_background.png")


def load_image(path: str, invert: bool = True, tint_color: tuple[int, int, int] = None) -> Image.Image:
    image = Image.open(path)
    if invert:
        if image.mode == 'RGBA':
            r,g,b,a = image.split()
            rgb_image = Image.merge('RGB', (r,g,b))
            output_image = ImageOps.invert(rgb_image)
            r2,g2,b2 = output_image.split()
            output_image = Image.merge('RGBA', (r2,g2,b2,a))
        else:
            output_image = ImageOps.invert(image)
    if tint_color is not None:
        output_image = tint_image(output_image, tint_color)
    return output_image


METEOR_SPRITE_1 = arcade.Texture(load_image("assets/sprites/asteroid.png"))
METEOR_SPRITE_2 = arcade.Texture(load_image("assets/sprites/meteor.png"))
SPACESHIP_SPRITE = arcade.Texture(load_image("assets/sprites/spaceship_2.png"))
BULLET_SPRITE = arcade.Texture(load_image("assets/sprites/bullet.png"))
USER_PROFILE_SPRITE = arcade.Texture(
    load_image("assets/sprites/account.png", tint_color=BROWN[:3])
)
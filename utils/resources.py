import arcade
from PIL import Image, ImageOps


SEPIA_BACKGROUND = arcade.load_texture("assets/sepia_background.png")

def load_and_invert_image(path):
    image = Image.open(path)
    if image.mode == 'RGBA':
        r,g,b,a = image.split()
        rgb_image = Image.merge('RGB', (r,g,b))
        inverted_image = ImageOps.invert(rgb_image)
        r2,g2,b2 = inverted_image.split()
        inverted_image = Image.merge('RGBA', (r2,g2,b2,a))
    else:
        inverted_image = ImageOps.invert(image)
    return inverted_image

METEOR_SPRITE_1 = arcade.Texture(load_and_invert_image("assets/sprites/asteroid.png"))
METEOR_SPRITE_2 = arcade.Texture(load_and_invert_image("assets/sprites/meteor.png"))
SPACESHIP_SPRITE = arcade.Texture(load_and_invert_image("assets/sprites/spaceship_2.png"))
BULLET_SPRITE = arcade.Texture(load_and_invert_image("assets/sprites/bullet.png"))
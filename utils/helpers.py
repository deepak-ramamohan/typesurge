import math
import arcade
from PIL import Image, ImageOps, ImageChops


def calculate_angle_between_points(point1, point2):
    """
    Calculate the angle (in radians, anticlockwise) of the line: (point1 -> point2)
    """
    dy = point2[1] - point1[1]
    dx = point2[0] - point1[0]
    theta = math.atan2(dy, dx)
    return theta


def tint_image(image: Image.Image, color: tuple[int, int, int]) -> Image.Image:
    """
    Applies a multiplicative tint to a PIL Image.
    This replicates the logic of arcade.Sprite.color.
    """
    # Make sure image is RGBA
    if image.mode != "RGBA":
        image = image.convert("RGBA")
        
    # Create a new solid-color image of the same size.
    # The tint color must include an Alpha channel (255 for solid).
    tint_layer = Image.new("RGBA", image.size, color + (255,))
    
    # Multiply the original image with the tint layer
    tinted_image = ImageChops.multiply(image, tint_layer)
    
    # The multiplication also multiplies the alpha channels, which
    # can make semi-transparent areas *more* transparent.
    # To avoid this and keep the original's transparency,
    # we can composite the tinted image back onto a transparent
    # background, using the original's alpha as the mask.
    
    # Create a new transparent image
    final_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
    
    # Paste the tinted image, but use the *original* image's alpha channel as the mask
    final_image.paste(tinted_image, (0, 0), mask=image.getchannel("A"))
    
    return final_image


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
    arcade.key.SPACE: " ",
    arcade.key.COMMA: ",",
    arcade.key.PERIOD: ".",
    arcade.key.SLASH: "/",
    arcade.key.COLON: ";",
    arcade.key.QUOTELEFT: "'",
    arcade.key.BRACKETLEFT: "[",
    arcade.key.BRACKETRIGHT: "]"
}

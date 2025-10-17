import math
import arcade


def calculate_angle_between_points(point1, point2):
    """
    Calculate the angle (in radians, anticlockwise) of the line: (point1 -> point2)
    """
    dy = point2[1] - point1[1]
    dx = point2[0] - point1[0]
    theta = math.atan2(dy, dx)
    return theta


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

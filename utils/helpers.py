import math


def calculate_angle_between_points(point1, point2):
    """
    Calculate the angle (in radians, anticlockwise) of the line: (point1 -> point2)
    """
    dy = point2[1] - point1[1]
    dx = point2[0] - point1[0]
    theta = math.atan2(dy, dx)
    return theta
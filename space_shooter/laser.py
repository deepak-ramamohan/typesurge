import arcade
import math
from utils.resources import LASER_SPRITE, LASER_SOUND
from utils.helpers import calculate_angle_between_points
from space_shooter.player import Player
from space_shooter.enemies import EnemyWord


class Laser(arcade.Sprite):
    """
    Spawns a laser that starts from a player position and moves towards the target
    """
    
    def __init__(
        self, 
        player: Player, 
        target: EnemyWord,
        speed: float = 30.0
    ) -> None:
        super().__init__(
            LASER_SPRITE,
            center_y=player.center_y,
            scale=0.8
        )
        self.left = player.right
        self.speed = speed
        self.target = target
        theta = calculate_angle_between_points(self.position, target.position)
        LASER_ANGLE_OFFSET = 90
        self.velocity = (
            self.speed * math.cos(theta),
            self.speed * math.sin(theta)
        )
        self.angle = math.degrees(2 * math.pi - theta) + LASER_ANGLE_OFFSET
        arcade.play_sound(LASER_SOUND)

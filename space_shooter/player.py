import arcade
from utils.resources import (
    SPACESHIP_SPRITE, 
    SPACESHIP_DAMAGE_SPRITE_1, 
    SPACESHIP_DAMAGE_SPRITE_2
)


class Player(arcade.Sprite):
    """
    The player sprite.
    """

    def __init__(self, center_x: float, center_y: float) -> None:
        """
        Initializer
        """
        ANGLE = 90
        SCALE = 0.8
        super().__init__(
            SPACESHIP_SPRITE,
            center_x=center_x,
            center_y=center_y,
            angle=ANGLE,
            scale=SCALE
        )
        self.damage_sprite_1 = arcade.Sprite(
            SPACESHIP_DAMAGE_SPRITE_1,
            center_x=center_x,
            center_y=center_y,
            angle=ANGLE,
            scale=SCALE
        )
        self.damage_sprite_2 = arcade.Sprite(
            SPACESHIP_DAMAGE_SPRITE_2,
            center_x=center_x,
            center_y=center_y,
            angle=ANGLE,
            scale=SCALE
        )
        self.MAX_LIVES = 3
        self.lives_remaining = self.MAX_LIVES

    def draw(self) -> None:
        """
        Draw the player sprite, with appropriate damage
        """
        arcade.draw_sprite(self)
        if self.lives_remaining == 2:
            arcade.draw_sprite(self.damage_sprite_1)
        elif self.lives_remaining == 1:
            arcade.draw_sprite(self.damage_sprite_2)

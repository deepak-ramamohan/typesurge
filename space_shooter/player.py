import arcade
from utils.colors import BROWN
from utils.resources import SPACESHIP_SPRITE


class Player(arcade.Sprite):
    """
    The player sprite.
    """

    def __init__(self, center_x: float, center_y: float) -> None:
        """
        Initializer
        """
        super().__init__(
            SPACESHIP_SPRITE,
            center_x=center_x,
            center_y=center_y,
            angle=90,
            scale=0.7
        )
        self.color = BROWN
        self.MAX_LIVES = 3
        self.lives_remaining = self.MAX_LIVES

    def reset_lives(self) -> None:
        """
        Reset the player's lives.
        """
        self.lives_remaining = self.MAX_LIVES
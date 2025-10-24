import arcade
from utils.colors import BROWN
from utils.resources import SPACESHIP_SPRITE


class Player(arcade.Sprite):

    def __init__(self, center_x, center_y):
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

    def reset_lives(self):
        self.lives_remaining = self.MAX_LIVES
import arcade
from utils.colors import BEIGE


class Player(arcade.Sprite):

    def __init__(self, center_x, center_y):
        super().__init__(
            ":resources:/images/space_shooter/playerShip2_orange.png",
            center_x=center_x,
            center_y=center_y,
            angle=90,
        )
        self.color = BEIGE
        self.MAX_LIVES = 3
        self.lives_remaining = self.MAX_LIVES

    def reset_lives(self):
        self.lives_remaining = self.MAX_LIVES
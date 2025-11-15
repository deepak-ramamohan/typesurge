import arcade
from utils.resources import EXPLOSION_SOUND, EXPLOSION_TEXTURE_LIST


class Explosion(arcade.Sprite):
    """
    An explosion animation.
    """

    def __init__(self) -> None:
        """
        Initializer
        """
        super().__init__(EXPLOSION_TEXTURE_LIST[0])
        self.time_elapsed = 0
        self.animation_time = 0.6
        self.textures = EXPLOSION_TEXTURE_LIST
        self._play_sound()

    def update(self, delta_time: float = 1 / 60) -> None:
        """
        Update the explosion animation.
        """
        self.time_elapsed += delta_time
        if self.time_elapsed <= self.animation_time:
            index = int(len(self.textures) * (self.time_elapsed / self.animation_time))
            self.set_texture(index)
        else:
            self.remove_from_sprite_lists()

    def _play_sound(self) -> None:
        """
        Play explosion sound
        """
        arcade.play_sound(EXPLOSION_SOUND)

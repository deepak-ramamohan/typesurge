import arcade


class Explosion(arcade.Sprite):
    """
    An explosion animation.
    """

    def __init__(self, texture_list: list[arcade.Texture]) -> None:
        """
        Initializer
        """
        super().__init__(texture_list[0])
        self.time_elapsed = 0
        self.animation_time = 0.6
        self.textures = texture_list

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

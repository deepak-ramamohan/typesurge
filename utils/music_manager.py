import arcade
from utils import global_state

class MusicManager:
    """
    Manages playing and stopping music.
    """

    @classmethod
    def play_music(cls, music: arcade.Sound, loop: bool = True) -> None:
        """
        Plays the given music.

        Args:
            music: The music to play.
            loop: Whether to loop the music.
        """
        cls.stop_current_music()
        global_state.current_music.sound = music
        global_state.current_music.player = arcade.play_sound(music, loop=loop)
        global_state.current_music.player.seek(0.0)

    @classmethod
    def stop_current_music(cls) -> None:
        """
        Stops the currently playing music.
        """
        if global_state.current_music.player is not None:
            arcade.stop_sound(global_state.current_music.player)
            global_state.current_music.player.delete()
        global_state.current_music.player = None
        global_state.current_music.sound = None

    @classmethod
    def is_music_playing_same(cls, music: arcade.Sound) -> bool:
        """
        Checks if the given music is the same as the currently playing music.
        """
        return global_state.current_music.sound == music

from utils.user_profile import UserProfile
import arcade
from pyglet.media import Player
from dataclasses import dataclass

current_user_profile: UserProfile

@dataclass
class CurrentMusic:
    """
    Holds the current music and player.
    """
    sound: arcade.Sound | None = None
    player: Player | None = None

current_music = CurrentMusic()
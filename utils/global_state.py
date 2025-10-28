from utils.user_profile import UserProfile
import arcade
from pyglet.media import Player
from dataclasses import dataclass

current_user_profile: UserProfile | None = None

@dataclass
class CurrentMusic:
    sound: arcade.Sound | None = None
    player: Player | None = None

current_music = CurrentMusic()
from dataclasses import dataclass


@dataclass
class UserProfile:
    """
    Represents a user profile.
    """
    name: str
    display_name: str
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterable, SupportsIndex
from collections import UserList


@dataclass
class GameStats:
    """
    Game stats for the space shooter
    """
    game_start_time: datetime = field(default_factory=datetime.now)
    score: int = 0


class GameStatsList(UserList):
    """
    A list of GameStats objects.
    """

    def _check_type(self, item: Any) -> None:
        """A reusable method to check the type"""
        if not isinstance(item, GameStats):
            raise TypeError(f"This list accepts only GameStats object, not {type(item).__name__}")
        
    def append(self, item: Any) -> None:
        self._check_type(item)
        return self.data.append(item)
    
    def insert(self, i: SupportsIndex, item: Any) -> None:
        self._check_type(item)
        return self.data.insert(i, item)
    
    def extend(self, other: Iterable) -> None:
        for item in other:
            self.append(item)

    def __setitem__(self, key: SupportsIndex | slice, value: Any) -> None:
        if isinstance(key, slice):
            for item in value:
                self._check_type(item)
        else:
            self._check_type(value)
        self.data[key] = value

    def get_high_score(self) -> int:
        """
        Returns the highest score from all the previous game sessions
        """
        high_score = 0
        if self.data:
            high_score = max(gs.score for gs in self.data)
        return high_score

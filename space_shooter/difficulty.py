import math
from dataclasses import dataclass


class Difficulty:
    """
    A class for managing game difficulty
    """

    @dataclass
    class EnemyCount:
        min: int = 2
        max: int = 5

    @dataclass
    class EnemyWordLength:
        min: int = 3
        max: int = 6

    @dataclass
    class EnemyMovementSpeed:
        min: float = 0.75
        max: float = 1.25

    @dataclass
    class DifficultySetting:
        ec_start: tuple[int, int]
        ec_increment: tuple[float, float]
        ec_limit: tuple[int, int]
        ewl_start: tuple[int, int]
        ewl_increment: tuple[float, float]
        ewl_limit: tuple[int, int]
        ems_start: tuple[float, float]
        ems_increment: tuple[float, float]
        ems_limit: tuple[float, float]
        multiplier_streak: int
        multiplier_limit: float

    def __init__(self, difficulty_level: int = 1) -> None:
        self.enemy_count = self.EnemyCount()
        self.enemy_word_length = self.EnemyWordLength()
        self.enemy_movement_speed = self.EnemyMovementSpeed()
        self.difficulty_setting = self._init_difficulty_setting(difficulty_level)
        self.update_difficulty(0.0)

    def _init_difficulty_setting(self, difficulty_level) -> DifficultySetting:
        easy = self.DifficultySetting(
            ec_start=(1, 2),
            ec_increment=(1/2000, 1/2000),
            ec_limit=(4, 5),
            ewl_start=(3, 5),
            ewl_increment=(1/4000, 1/3000),
            ewl_limit=(5, 8),
            ems_start=(0.7, 1.0),
            ems_increment=(0.1/3000, 0.1/3000),
            ems_limit=(1.4, 1.8),
            multiplier_streak=5,
            multiplier_limit=2.0
        )
        moderate = self.DifficultySetting(
            ec_start=(2, 4),
            ec_increment=(1/4000, 1/4000),
            ec_limit=(4, 6),
            ewl_start=(4, 6),
            ewl_increment=(1/4000, 1/3000),
            ewl_limit=(5, 10),
            ems_start=(0.75, 1.25),
            ems_increment=(0.1/6000, 0.1/6000),
            ems_limit=(1.5, 2.0),
            multiplier_streak=2,
            multiplier_limit=5.0
        )
        hard = self.DifficultySetting(
            ec_start=(4, 5),
            ec_increment=(1/8000, 1/8000),
            ec_limit=(5, 7),
            ewl_start=(5, 8),
            ewl_increment=(1/8000, 1/10000),
            ewl_limit=(7, 15),
            ems_start=(1.0, 1.5),
            ems_increment=(0.1/10000, 0.1/10000),
            ems_limit=(1.75, 2.5),
            multiplier_streak=1,
            multiplier_limit=10.0
        )
        self.difficulty_settings = [
            easy,
            moderate,
            hard
        ]
        return self.difficulty_settings[difficulty_level]

    def _calculate_score_based_values(
        self,
        score: float | int,
        start: tuple,
        increment: tuple,
        limit: tuple,
        as_int: bool = False
    ) -> tuple:
        """
        Helper function for calculating a 2-tuple of values.
        Uses the score and the predefined 2-tuples: start, increment and limits
        """
        values = tuple(min(start[i] + score * increment[i], limit[i]) for i in range(2))
        if as_int:
            values = tuple(math.floor(value) for value in values)
        # Edge case: if the min values is growing faster than the max
        if values[0] > values[1]:
            values = (values[1], values[1])
        return values

    def update_difficulty(self, score: float) -> None:
        """
        Updates the difficulty setting values based on the score
        """
        self.enemy_count.min, self.enemy_count.max = self._calculate_score_based_values(
            score,
            self.difficulty_setting.ec_start,
            self.difficulty_setting.ec_increment,
            self.difficulty_setting.ec_limit,
            as_int=True
        )
        self.enemy_word_length.min, self.enemy_word_length.max = self._calculate_score_based_values(
            score,
            self.difficulty_setting.ewl_start,
            self.difficulty_setting.ewl_increment,
            self.difficulty_setting.ewl_limit,
            as_int=True
        )
        self.enemy_movement_speed.min, self.enemy_movement_speed.max = self._calculate_score_based_values(
            score,
            self.difficulty_setting.ems_start,
            self.difficulty_setting.ems_increment,
            self.difficulty_setting.ems_limit,
            as_int=False
        )
        # print(f"Difficulty updated: {self.enemy_count}, {self.enemy_word_length}, {self.enemy_movement_speed}")

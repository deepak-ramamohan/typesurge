from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime
from typing import Any, Iterable, SupportsIndex
from collections import UserList
import pandas as pd
import numpy as np


@dataclass
class SessionStats:
    """
    Statistics for a single AI trainer session.
    """
    session_start_time: datetime = field(default_factory=datetime.now)
    char_confusion_matrix: defaultdict[str, defaultdict[str, int]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(int))
    )
    char_times: defaultdict[str, list] = field(default_factory=lambda: defaultdict(list))
    wpm: float = 0.0
    word_mistype_counts: defaultdict[str, int] = field(default_factory=lambda: defaultdict(int))
    chars_typed_correctly: int = 0
    chars_typed_total: int = 0
    accuracy: float = 0.0
    duration_seconds: float = 0.0


class SessionStatsList(UserList):
    """
    A list of SessionStats objects.
    Contains helpful functions for aggregation
    """

    def _check_type(self, item: Any) -> None:
        """A reusable method to check the type"""
        if not isinstance(item, SessionStats):
            raise TypeError(f"This list accepts only SessionStats object, not {type(item).__name__}")
        
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

    def collect_char_times(self) -> dict[str, list]:
        result = defaultdict(list)
        for stats in self.data:
            for char, times in stats.char_times.items():
                result[char].extend(times)
        return result
    
    def compute_overall_confusion_matrix(self) -> defaultdict[str, defaultdict[str, int]]:
        """
        Aggregates all of the session-level confusion matrices.
        
        Returns an overall confusion matrix corresponding to all of the sessions 
        present in the list
        """
        overall_confusion_matrix = defaultdict(lambda: defaultdict(int))
        for session in self.data:
            for char, counts in session.char_confusion_matrix.items():
                for typed_char, count in counts.items():
                    overall_confusion_matrix[char][typed_char] += count
        return overall_confusion_matrix
    
    def compute_aggregate_char_metrics(self) -> pd.DataFrame:
        """
        Returns a pandas dataframe with aggregated metrics 
        from all the sessions in the list
        """
        metrics_list = []
        confusion_matrix = self.compute_overall_confusion_matrix()
        char_times = self.collect_char_times()
        for char, counts in confusion_matrix.items():
            count_correct, count_total = counts[char], sum(counts.values())
            mean_flight_time = np.mean(char_times[char]) if char_times[char] else 10.0
            data = {
                "char": char,
                "count_total": count_total,
                "count_correct": count_correct,
                "accuracy": count_correct / count_total,
                "mean_flight_time": mean_flight_time,
                "char_wpm": 12 / mean_flight_time
            }
            metrics_list.append(data)
        metrics_df = pd.DataFrame(metrics_list)
        if metrics_df.shape[0] > 0:
            metrics_df.set_index("char", inplace=True)
        return metrics_df

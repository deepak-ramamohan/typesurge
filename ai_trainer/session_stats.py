from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime


@dataclass
class SessionStats:
    session_start_time: datetime = field(default_factory=datetime.now)
    char_confusion_matrix: defaultdict[str, defaultdict[str, int]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(int))
    )
    char_times: defaultdict[str, list] = field(default_factory=lambda: defaultdict(list))
    wpm: float = 0.0
    word_mistype_count: defaultdict[str, int] = field(default_factory=lambda: defaultdict(int))
    chars_typed_correctly: int = 0
    chars_typed_total: int = 0
    accuracy: float = 0.0
    duration_seconds: float = 0.0

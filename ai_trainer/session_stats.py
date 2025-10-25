import os
import json
from dataclasses import dataclass, field, asdict
from collections import defaultdict


@dataclass
class SessionStats:
    char_confusion_matrix: defaultdict[str, defaultdict[str, int]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(int))
    )
    wpm: int = 0
    words_typed: int = 0
    chars_typed_correctly: int = 0
    chars_typed_total: int = 0
    accuracy: float = 0.0
    duration_seconds: float = 0.0


def save_session_stats(
    session_stats: SessionStats, 
    save_folder: str
) -> None:
    filename = "save.json"
    save_path = os.path.join(save_folder, filename)
    with open(save_path, "w") as file:
        json.dump(asdict(session_stats), file, indent=4)
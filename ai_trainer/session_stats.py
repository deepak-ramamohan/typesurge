import os
import json
import sqlite3
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from datetime import datetime


@dataclass
class SessionStats:
    session_start_time: datetime = field(default_factory=datetime.now)
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
        json.dump(asdict(session_stats), file, indent=4, default=str)


DB_FILE = "save.db"


def create_database() -> None:
    """
    Creates the database and session_stats table if it doesn't exist
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS session_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_start_time TIMESTAMP NOT NULL,
        char_confusion_matrix TEXT,
        wpm REAL,
        words_typed INTEGER,
        chars_typed_correctly INTEGER,
        chars_typed_total INTEGER,
        accuracy REAL,
        duration_seconds REAL
    )
    """
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)


def save_session_stats_to_db(session_stats: SessionStats) -> None:
    insert_query = """
    INSERT INTO session_stats (
        session_start_time, 
        char_confusion_matrix,
        wpm,
        words_typed,
        chars_typed_correctly,
        chars_typed_total,
        accuracy,
        duration_seconds
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    stats_dict = asdict(session_stats)
    data_tuple = (
        stats_dict["session_start_time"],
        json.dumps(stats_dict["char_confusion_matrix"]),
        stats_dict["wpm"],
        stats_dict["words_typed"],
        stats_dict["chars_typed_correctly"],
        stats_dict["chars_typed_total"],
        stats_dict["accuracy"],
        stats_dict["duration_seconds"]
    )
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(insert_query, data_tuple)
        conn.commit()


def load_db():
    result = None
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM session_stats")
        result = cursor.fetchall()
    print(result)

import sqlite3
import os
import json
from utils.user_profile import UserProfile
from ai_trainer.session_stats import SessionStats
from dataclasses import asdict


class SaveManager:

    SAVE_FOLDER = "save/"

    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        filename = user_profile.name + ".db"
        os.makedirs(self.SAVE_FOLDER, exist_ok=True)
        self.file_path = os.path.join(self.SAVE_FOLDER, filename)
        self.init_db()

    def init_db(self) -> None:
        """
        Initializes the database and creates tables if they don't exist
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS trainer_session_stats (
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
        with sqlite3.connect(self.file_path) as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)

    def save_session_stats_to_db(self, session_stats: SessionStats) -> None:
        insert_query = """
        INSERT INTO trainer_session_stats (
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
        with sqlite3.connect(self.file_path) as conn:
            cursor = conn.cursor()
            cursor.execute(insert_query, data_tuple)
            conn.commit()

    def load_and_print_db(self):
        result = None
        with sqlite3.connect(self.file_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM trainer_session_stats")
            result = cursor.fetchall()
        print(result)

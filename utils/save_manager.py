import sqlite3
import os
import json
from utils.user_profile import UserProfile
from ai_trainer.session_stats import SessionStats
from dataclasses import asdict
from collections import defaultdict


class SaveManager:
    """
    Manages saving and loading of user data and session stats.
    """

    SAVE_FOLDER = "save/"

    def __init__(self, user_profile: UserProfile):
        """
        Initializes the SaveManager.

        Args:
            user_profile: The user profile to manage.
        """
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
            char_times TEXT,
            wpm REAL,
            word_mistype_counts TEXT,
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
        """
        Saves the session stats to the database.

        Args:
            session_stats: The session stats to save.
        """
        insert_query = """
        INSERT INTO trainer_session_stats (
            session_start_time, 
            char_confusion_matrix,
            char_times,
            wpm,
            word_mistype_counts,
            chars_typed_correctly,
            chars_typed_total,
            accuracy,
            duration_seconds
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        stats_dict = asdict(session_stats)
        data_tuple = (
            stats_dict["session_start_time"],
            json.dumps(stats_dict["char_confusion_matrix"]),
            json.dumps(stats_dict["char_times"]),
            stats_dict["wpm"],
            json.dumps(stats_dict["word_mistype_counts"]),
            stats_dict["chars_typed_correctly"],
            stats_dict["chars_typed_total"],
            stats_dict["accuracy"],
            stats_dict["duration_seconds"]
        )
        with sqlite3.connect(self.file_path) as conn:
            cursor = conn.cursor()
            cursor.execute(insert_query, data_tuple)
            conn.commit()

    def load_and_print_db(self) -> None:
        """
        Loads and prints the entire database to the console.
        """
        result = None
        with sqlite3.connect(self.file_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM trainer_session_stats")
            result = cursor.fetchall()
        print(result)

    def get_char_accuracies(self) -> defaultdict:
        """
        Gets the character accuracies from the database.
        """
        query = """
        SELECT char_confusion_matrix FROM trainer_session_stats
        """
        confusion_matrix = defaultdict(lambda: defaultdict(int))
        with sqlite3.connect(self.file_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            for row in cursor.fetchall():
                for char, counts in json.loads(row["char_confusion_matrix"]).items():
                    for typed_char, count in counts.items():
                        confusion_matrix[char][typed_char] += count
        char_accuracy = defaultdict(float)
        for char, counts in confusion_matrix.items():
            char_accuracy[char] = counts[char] / sum(counts.values())
        return char_accuracy
    
    def get_word_mistype_counts(self) -> defaultdict:
        """
        Gets the word mistype counts from the database.
        """
        query = """
        SELECT word_mistype_counts FROM trainer_session_stats
        """
        word_mistype_counts = defaultdict(int)
        with sqlite3.connect(self.file_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            for row in cursor.fetchall():
                for word, count in json.loads(row["word_mistype_counts"]).items():
                    word_mistype_counts[word] += count
        return word_mistype_counts

    def get_all_session_stats(self) -> list[SessionStats]:
        """
        Gets all session stats from the database.
        """
        query = "SELECT * FROM trainer_session_stats ORDER BY session_start_time"
        session_stats_list = []
        with sqlite3.connect(self.file_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            for row in cursor.fetchall():
                session_stats_list.append(
                    SessionStats(
                        session_start_time=row["session_start_time"],
                        char_confusion_matrix=json.loads(row["char_confusion_matrix"]),
                        char_times=json.loads(row["char_times"]),
                        wpm=row["wpm"],
                        word_mistype_counts=json.loads(row["word_mistype_counts"]),
                        chars_typed_correctly=row["chars_typed_correctly"],
                        chars_typed_total=row["chars_typed_total"],
                        accuracy=row["accuracy"],
                        duration_seconds=row["duration_seconds"],
                    )
                )
        return session_stats_list

import pytest
import sqlite3
import json
from collections import defaultdict
from utils.save_manager import SaveManager
from utils.user_profile import UserProfile
from ai_trainer.session_stats import SessionStats

@pytest.fixture
def temp_db(tmp_path):
    """Fixture to create a temporary database for testing."""
    db_path = tmp_path / "test.db"
    return str(db_path)

@pytest.fixture
def user_profile():
    """Fixture to create a mock UserProfile."""
    return UserProfile(name="test_user", display_name="Test User")

@pytest.fixture
def session_stats():
    """Fixture to create a mock SessionStats object."""
    stats = SessionStats()
    stats.wpm = 100.0
    stats.accuracy = 0.95
    stats.char_confusion_matrix = defaultdict(lambda: defaultdict(int), {'a': {'s': 1, 'a': 1}}) # Added 'a' for accuracy test
    stats.word_mistype_counts = defaultdict(int, {'hello': 2})
    return stats

def test_init_db(temp_db, user_profile):
    """Test that the database is initialized correctly."""
    user_profile.name = "init_test"
    save_manager = SaveManager(user_profile)
    # Overwrite the file_path to use the temporary database
    save_manager.file_path = temp_db
    save_manager.init_db()

    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trainer_session_stats';")
        assert cursor.fetchone() is not None

def test_save_and_load_stats(temp_db, user_profile, session_stats):
    """Test saving and loading of session stats."""
    save_manager = SaveManager(user_profile)
    save_manager.file_path = temp_db
    # Manually initialize the database in the temporary location
    save_manager.init_db()

    # Save the stats
    save_manager.save_session_stats_to_db(session_stats)

    # Verify the saved data
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trainer_session_stats")
        row = cursor.fetchone()
        assert row is not None
        assert row[4] == 100.0  # WPM
        assert json.loads(row[2])['a']['s'] == 1 # char_confusion_matrix

    # Test retrieval functions
    char_accuracies = save_manager.get_char_accuracies()
    # 'a' was typed once correctly and once incorrectly ('s')
    assert char_accuracies['a'] == 0.5

    word_mistype_counts = save_manager.get_word_mistype_counts()
    assert word_mistype_counts['hello'] == 2

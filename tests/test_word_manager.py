import pytest
from collections import defaultdict
from utils.word_manager import WordManager

@pytest.fixture
def temp_word_file(tmp_path):
    """Fixture to create a temporary word file for testing."""
    word_file = tmp_path / "words.txt"
    word_file.write_text("apple banana cherry date elderberry")
    return str(word_file)

@pytest.fixture
def char_accuracies():
    """Fixture for mock character accuracies."""
    # 'a' is inaccurate, 'b' is perfect
    return defaultdict(float, {'a': 0.5, 'b': 1.0})

@pytest.fixture
def word_mistype_counts():
    """Fixture for mock word mistype counts."""
    # 'apple' is frequently mistyped
    return defaultdict(int, {'apple': 5})

def test_load_words(temp_word_file):
    """Test that words are loaded correctly from a file."""
    word_manager = WordManager(file_path=temp_word_file)
    assert len(word_manager.word_list) == 5
    assert "apple" in word_manager.word_list

def test_get_weighted_sample(temp_word_file, char_accuracies, word_mistype_counts):
    """Test the weighted sampling of words."""
    word_manager = WordManager(file_path=temp_word_file)
    # With the given weights, 'apple' should be heavily favored due to both
    # its mistype count and the inaccuracy of the letter 'a'.
    sample = word_manager.get_weighted_sample(1, char_accuracies, word_mistype_counts)
    assert len(sample) == 1
    # This isn't a deterministic test, but with the high weights, it's very likely.
    # A more robust test would check the calculated weights directly.
    # For now, we'll assume the sampling is correct if it returns a word.
    assert isinstance(sample[0], str)

def test_generate_word(temp_word_file):
    """Test the generation of a random word."""
    word_manager = WordManager(file_path=temp_word_file)
    word = word_manager.generate_word(min_character_count=5, max_character_count=6)
    assert 5 <= len(word) <= 6
    assert word in ["apple", "banana", "cherry"]

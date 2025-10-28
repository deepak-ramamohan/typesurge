import random
from collections import defaultdict


class WordManager:
    """Class for loading and managing words"""

    def __init__(self, file_path="words_v1.txt"):
        self._load_words(file_path)
        self._split_word_list_by_character_count()

    def _load_words(self, file_path):
        """
        Load the words from the text file.
        """
        self.word_list = []
        with open(file_path, 'r') as file:
            self.word_list = list(set(file.read().split()))
    
    def _split_word_list_by_character_count(self):
        self.character_count_dict = defaultdict(list)
        for word in self.word_list:
            self.character_count_dict[len(word)].append(word)

    def generate_word(self, min_character_count=4, max_character_count=7):
        """
        Generate new words by sampling from the existing list
        """
        character_count = random.randint(min_character_count, max_character_count)
        word = random.choice(self.character_count_dict[character_count])
        return word
    
import random
import math
from collections import defaultdict


class WordManager:
    """Class for loading and managing words"""

    # --- Weight Calculation Constants ---
    # These can be tuned to change the behavior of the word sampling.

    # Controls the influence of the word's general difficulty based on its characters.
    WEIGHT_CHAR_SCORE = 0.5
    # Controls how much influence a word's specific mistype history has.
    WEIGHT_WORD_SCORE = 1.0
    # A base weight for all words to ensure new/easy words still have a chance to appear.
    WEIGHT_BASE = 0.01

    def __init__(self, file_path="words_v1.txt"):
        self._load_words(file_path)
        self._group_words_by_length()

    def _load_words(self, file_path):
        """
        Load the words from the text file.
        """
        self.word_list = []
        with open(file_path, 'r') as file:
            self.word_list = list(set(file.read().split()))
    
    def _group_words_by_length(self):
        self.words_by_length = defaultdict(list)
        for word in self.word_list:
            self.words_by_length[len(word)].append(word)

    def _calculate_word_weights(self, word_list, char_accuracies, word_mistype_counts, weight_base_multiplier=1.0):
        """
        Calculates a weight for each word in the provided list based on user stats.
        """
        weighted_word_list = []
        for word in word_list:
            # Calculate character_score for the word
            character_score = 0
            for char in word:
                accuracy = char_accuracies.get(char, 1.0) # Default to 1.0 accuracy if char not in stats
                char_score = math.log(1 + 10 * (1 - accuracy) * 100)
                character_score += char_score

            # Calculate word_score for the word
            mistype_count = word_mistype_counts.get(word, 0)
            word_score = math.log(1 + 10 * min(mistype_count, 50))

            # Calculate final hybrid weight
            final_weight = (self.WEIGHT_CHAR_SCORE * character_score) + \
                           (self.WEIGHT_WORD_SCORE * word_score) + \
                           self.WEIGHT_BASE * weight_base_multiplier
            
            weighted_word_list.append((word, final_weight))
        
        return weighted_word_list

    def get_weighted_sample(self, num_words, char_accuracies, word_mistype_counts, min_character_count=1, max_character_count=99):
        """
        Generates a list of words using a weighted sampling algorithm.

        This method uses the single-pass sorting method (Efraimidis and Spirakis)
        for efficient weighted random sampling without replacement.

        Args:
            num_words (int): The number of words to sample.
            char_accuracies (dict): A dictionary mapping characters to their accuracy.
            word_mistype_counts (dict): A dictionary mapping words to their mistype count.
            min_character_count (int): The minimum length of words to include.
            max_character_count (int): The maximum length of words to include.

        Returns:
            list: A list of unique words.
        """
        # First, filter the word list by length using the pre-computed dictionary.
        filtered_word_list = []
        for length in range(min_character_count, max_character_count + 1):
            filtered_word_list.extend(self.words_by_length.get(length, []))

        if not filtered_word_list:
            return []

        # Phase 2: Calculate weights for the filtered list of words
        weighted_words = self._calculate_word_weights(filtered_word_list, char_accuracies, word_mistype_counts)

        # Phase 3: Implement the single-pass sorting method
        scored_words = []
        for word, weight in weighted_words:
            random_val = random.random()
            score = random_val ** (1 / weight)
            scored_words.append((word, score))
        
        # Sort by the calculated score in descending order
        scored_words.sort(key=lambda x: x[1], reverse=True)

        # Select the top `num_words`
        num_to_sample = min(num_words, len(scored_words))
        final_word_list = [word for word, score in scored_words[:num_to_sample]]

        return final_word_list

    def generate_word(self, min_character_count=4, max_character_count=7):
        """
        Generate new words by sampling from the existing list
        """
        character_count = random.randint(min_character_count, max_character_count)
        word = random.choice(self.words_by_length[character_count])
        return word
      
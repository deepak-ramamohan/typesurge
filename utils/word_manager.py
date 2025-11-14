import random
import pandas as pd
from collections import defaultdict


def calculate_char_weights(char_metrics_df: pd.DataFrame, noise: float = 1.0) -> defaultdict[str, float]:
    """
    Calculates weights for each character based on accuracy.
    """
    if char_metrics_df.shape[0] > 0:
        weights = char_metrics_df.apply(
            lambda x: 100 * (1 - x['accuracy']) +\
                0.5 * min(100.0, x['mean_flight_time'] * 50) +\
                10.0 * int(x['count_total'] < 50) +\
                noise * random.gauss(), 
            axis=1
        )
        char_weights = defaultdict(
            lambda: 10.0,
            weights.to_dict()
        )
    else:
        char_weights = defaultdict(lambda: 1.0)
    # print(char_weights)
    return char_weights


def calculate_word_weights(word_mistype_counts, weight_decay_exponent=1.1):
    """
    Calculates weights for each word based on mistype counts.
    """
    sorted_mistype_counts = sorted(word_mistype_counts.items(), key=lambda x: x[1], reverse=True)
    weight = 1.0
    decay_limit = 10
    decay_count = 0
    word_weights = defaultdict(lambda: weight / weight_decay_exponent**decay_limit) # Default weight
    for word, _ in sorted_mistype_counts:
        word_weights[word] = weight
        if decay_count < decay_limit:
            weight /= weight_decay_exponent
            decay_count += 1
    # print(word_weights)
    return word_weights


class WordManager:
    """Class for loading and managing words"""

    # --- Weight Calculation Constants ---
    WEIGHT_CHAR_SCORE = 1.0
    WEIGHT_WORD_SCORE = 0.0
    WEIGHT_RANDOM = 2.0

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

    def _calculate_hybrid_word_weights(self, word_list, char_weights, word_weights, weight_base_multiplier=1.0):
        """
        Calculates a hybrid weight for each word based on character and word weights.
        """
        weighted_word_list = []
        for word in word_list:
            character_score = sum(char_weights[char] for char in word) * 1.0 / len(word)
            word_score = word_weights[word]

            # Calculate final hybrid weight
            final_weight = (self.WEIGHT_CHAR_SCORE * character_score) + \
                           (self.WEIGHT_WORD_SCORE * word_score) + \
                           self.WEIGHT_RANDOM * random.gauss()

            weighted_word_list.append((word, final_weight))

        return weighted_word_list

    def get_weighted_sample(self, num_words, char_weights, word_weights, min_character_count=1, max_character_count=99):
        """
        Generates a list of words using a weighted sampling algorithm.

        Args:
            num_words (int): The number of words to sample.
            char_weights (defaultdict): A dictionary mapping characters to their weights.
            word_weights (defaultdict): A dictionary mapping words to their weights.
            min_character_count (int): The minimum length of words to include.
            max_character_count (int): The maximum length of words to include.

        Returns:
            list: A list of unique words.
        """
        filtered_word_list = []
        for length in range(min_character_count, max_character_count + 1):
            filtered_word_list.extend(self.words_by_length.get(length, []))

        if not filtered_word_list:
            return []

        weighted_words = self._calculate_hybrid_word_weights(filtered_word_list, char_weights, word_weights)

        scored_words = []
        for word, weight in weighted_words:
            # random_val = random.random()
            # score = random_val ** (1 / weight)
            score = weight
            scored_words.append((word, score))
        
        # Sort by the calculated score in descending order
        scored_words.sort(key=lambda x: x[1], reverse=True)

        # Select the top `num_words`
        num_to_sample = min(num_words, len(scored_words))
        final_word_list = [word for word, score in scored_words[:num_to_sample]]

        return final_word_list
    
    def get_random_sample(self, num_words, min_character_count=3, max_character_count=9):
        """
        Generates a list of words sampled randomly

        Args:
            num_words (int): The number of words to sample.
            min_character_count (int): The minimum length of words to include.
            max_character_count (int): The maximum length of words to include.

        Returns:
            list: A list of unique words.
        """
        filtered_word_list = []
        for length in range(min_character_count, max_character_count + 1):
            filtered_word_list.extend(self.words_by_length.get(length, []))

        if not filtered_word_list:
            return []
        
        final_word_list = random.sample(filtered_word_list, num_words)
        return final_word_list

    def generate_word(self, min_character_count=4, max_character_count=7):
        """
        Generate new words by sampling from the existing list
        """
        character_count = random.randint(min_character_count, max_character_count)
        word = random.choice(self.words_by_length[character_count])
        return word

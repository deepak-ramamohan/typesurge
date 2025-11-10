import random
import pandas as pd
from collections import defaultdict


def calculate_char_weights(char_metrics_df: pd.DataFrame, noise: float = 1.0) -> defaultdict[str, float]:
    """
    Calculates weights for each character based on accuracy.
    """
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
    print(char_weights)
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
    # These can be tuned to change the behavior of the word sampling.

    # Controls the influence of the word's general difficulty based on its characters.
    WEIGHT_CHAR_SCORE = 1.0
    # Controls how much influence a word's specific mistype history has.
    WEIGHT_WORD_SCORE = 1.0
    # A base weight for all words to ensure new/easy words still have a chance to appear.
    WEIGHT_RANDOM = 1.0

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
            # Calculate character_score for the word by summing the weights of its characters.
            character_score = sum(char_weights[char] for char in word)

            # Get the pre-calculated word_score for the word.
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

        This method uses the single-pass sorting method (Efraimidis and Spirakis)
        for efficient weighted random sampling without replacement.

        Args:
            num_words (int): The number of words to sample.
            char_weights (defaultdict): A dictionary mapping characters to their weights.
            word_weights (defaultdict): A dictionary mapping words to their weights.
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
        weighted_words = self._calculate_hybrid_word_weights(filtered_word_list, char_weights, word_weights)

        # Phase 3: Implement the single-pass sorting method
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

    def generate_word(self, min_character_count=4, max_character_count=7):
        """
        Generate new words by sampling from the existing list
        """
        character_count = random.randint(min_character_count, max_character_count)
        word = random.choice(self.words_by_length[character_count])
        return word

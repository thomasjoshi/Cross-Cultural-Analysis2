from collections import Counter
from math import log
import pandas as pd


class DataProcessor:
    @staticmethod
    def process(word_count: Counter):
        log_word_count = Counter()
        for word in word_count:
            log_word_count[word] = log(word_count[word])

        sorted_word_count = word_count.most_common()
        words = list(zip(*sorted_word_count))[0]
        counts = list(zip(*sorted_word_count))[1]
        indices = [i + 1 for i in range(len(word_count))]
        sorted_log_word_count = log_word_count.most_common()
        log_words = list(zip(*sorted_log_word_count))[0]
        log_counts = list(zip(*sorted_log_word_count))[1]
        log_indices = [log(i + 1) for i in range(len(log_word_count))]

        data = {'word': words, 'count': counts, 'index': indices}
        df = pd.DataFrame(data=data)

        log_data = {'word': log_words, 'count': log_counts, 'index': log_indices}
        log_df = pd.DataFrame(data=log_data)

        return df, log_df

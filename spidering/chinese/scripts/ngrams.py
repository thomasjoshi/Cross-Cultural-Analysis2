import jieba
from collections import Counter
import matplotlib.pyplot as plt


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def save_result(sorted_items, filename):
    with open(filename, 'w') as f:
        f.writelines(k + '\t' + str(v) + '\n' for k, v in sorted_items)


if __name__ == '__main__':
    keyword = 'alphago'
    filename = keyword + '_descriptions.txt'
    result_filename = keyword + '_token_counts.txt'
    texts = read_file(filename)
    tokens = Counter(jieba.cut(texts))
    sorted_items = sorted(tokens.items(), key=lambda x: x[1], reverse=True)
    save_result(sorted_items, result_filename)

    counts = [c[1] for c in sorted_items]
    plt.loglog(range(1, 1 + len(counts)), counts, 'o-')
    plt.show()

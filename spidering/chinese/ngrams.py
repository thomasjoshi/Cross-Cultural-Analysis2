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
    filenames = (
        'titles_iqiyi.txt', 'titles_qq.txt', 'titles_bilibili.txt', 'desc_iqiyi.txt', 'desc_qq.txt',
        'desc_bilibili.txt')
    result_filename = 'token_counts.txt'
    texts = (read_file(filename) for filename in filenames)
    tokens = Counter()
    for text in texts:
        tokens += Counter(jieba.cut(text))
    sorted_items = sorted(tokens.items(), key=lambda x: x[1], reverse=True)
    save_result(sorted_items, result_filename)

    counts = [c[1] for c in sorted_items]
    plt.loglog(range(1, 1 + len(counts)), counts, 'o-')
    plt.show()

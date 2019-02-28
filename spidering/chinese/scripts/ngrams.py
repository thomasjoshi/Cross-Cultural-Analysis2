import jieba
from collections import Counter
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 4:
    print('Usage: python3 script.py input.txt output.txt output.png')
    print('For example: python3 download.py alphago_descriptions.txt alphago_counts.txt alphago.png')
    sys.exit(1)


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def save_result(sorted_items, filename):
    with open(filename, 'w') as f:
        f.writelines(k + '\t' + str(v) + '\n' for k, v in sorted_items)


if __name__ == '__main__':
    filename = sys.argv[1]
    result_filename = sys.argv[2]
    png_filename = sys.argv[3]
    texts = read_file(filename)
    tokens = Counter(jieba.cut(texts))
    sorted_items = sorted(tokens.items(), key=lambda x: x[1], reverse=True)
    save_result(sorted_items, result_filename)

    counts = [c[1] for c in sorted_items]
    plt.loglog(range(1, 1 + len(counts)), counts, 'o')
    plt.savefig(png_filename)

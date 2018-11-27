import jieba
from collections import Counter


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


# def build_dict(text):
#     tokens = word_tokenize(text, 'chinese')
#     return tokens


def save_result(tokens, filename):
    with open(filename, 'w') as f:
        f.writelines(k + '\t' + str(v) + '\n' for k, v in sorted(tokens.items(), key=lambda x: x[1], reverse=True))


if __name__ == '__main__':
    filename = 'desc_iqiyi.txt'
    result_filename = 'token_counts.txt'
    text = read_file(filename)
    tokens = Counter(jieba.cut(text))
    save_result(tokens, result_filename)

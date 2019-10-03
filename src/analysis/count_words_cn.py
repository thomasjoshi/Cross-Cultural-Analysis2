#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import jieba
import matplotlib.pyplot as plt
import os
from collections import Counter


def count(input_filename, result_filename=None, plot_filename=None):
    with open(input_filename) as f:
        texts = f.read()
    tokens = Counter(t for t in jieba.cut(texts) if not t.isspace())
    sorted_items = sorted(tokens.items(), key=lambda x: x[1], reverse=True)

    if result_filename:
        dirname = os.path.dirname(result_filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        with open(result_filename, 'w') as f:
            f.writelines(f'{k}\t{v}\n' for k, v in sorted_items)

    if plot_filename:
        dirname = os.path.dirname(plot_filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        counts = [c[1] for c in sorted_items]
        plt.loglog(range(1, 1 + len(counts)), counts, 'o')
        plt.savefig(plot_filename)


def main():
    parser = argparse.ArgumentParser(description='parse and count Chinese words')
    parser.add_argument('input', help='input text file')
    parser.add_argument('-o', '--output', help='output results')
    parser.add_argument('-p', '--plot', help='output plot')
    args = parser.parse_args()
    count(args.input, args.output, args.plot)


if __name__ == '__main__':
    main()

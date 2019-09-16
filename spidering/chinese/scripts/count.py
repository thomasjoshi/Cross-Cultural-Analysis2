#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import jieba
from collections import Counter
import matplotlib.pyplot as plt
import argparse
import os
from parser import Parser

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='count Chinese words')
    parser.add_argument('input', help='input text file')
    parser.add_argument('-o', '--output', help='output results')
    parser.add_argument('-p', '--plot', help='output plot')
    args = parser.parse_args()

    input_filename = args.input
    result_filename = args.output
    png_filename = args.plot

    with open(input_filename) as f:
        texts = f.read().splitlines()
    texts = ' '.join(text for text in texts if text[:len(Parser.MARK)] != Parser.MARK)
    tokens = Counter(jieba.cut(texts))
    if ' ' in tokens:
        tokens.pop(' ')
    sorted_items = sorted(tokens.items(), key=lambda x: x[1], reverse=True)

    if result_filename:
        dirname = os.path.dirname(result_filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(result_filename, 'w') as f:
            f.writelines(k + '\t' + str(v) + '\n' for k, v in sorted_items)

    if png_filename:
        dirname = os.path.dirname(png_filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        counts = [c[1] for c in sorted_items]
        plt.loglog(range(1, 1 + len(counts)), counts, 'o')
        plt.savefig(png_filename)

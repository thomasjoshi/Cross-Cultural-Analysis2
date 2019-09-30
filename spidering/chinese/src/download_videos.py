#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from spider import Spider
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='download videos using metadata')
    parser.add_argument('input', help='input metadata file')
    parser.add_argument('-o', '--output', default='output', help='output directory')
    parser.add_argument('-s', '--sources', nargs='*', help='filter sources')
    args = parser.parse_args()

    input_file = args.input
    output = args.output
    sources = args.sources

    if not os.path.isdir(output):
        os.makedirs(output)

    parser = Spider()
    parser.load_data(input_file)
    parser.download(output, sources)

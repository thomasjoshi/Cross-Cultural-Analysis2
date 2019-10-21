#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import os
from spider import Spider


def download(input_file, output='output', sources=None):
    if not os.path.isdir(output):
        os.makedirs(output)
    spider = Spider()
    spider.load(input_file)
    spider.download(output, sources)


def main():
    parser = argparse.ArgumentParser(description='download videos using metadata')
    parser.add_argument('input', help='input metadata file')
    parser.add_argument('-o', '--output', default='output', help='output directory')
    parser.add_argument('-s', '--sources', nargs='*', help='filter sources')
    args = parser.parse_args()
    download(args.input, args.output, args.sources)


if __name__ == '__main__':
    main()

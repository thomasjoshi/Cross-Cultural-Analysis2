#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import json
import os


def process_transcript(trans_dir, output_path='output.json'):
    trans_type = 'json'
    output_dir = os.path.dirname(output_path)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    result = {}
    for trans_filename in os.listdir(trans_dir):
        if not trans_filename.endswith('.' + trans_type):
            continue
        dot_pos = trans_filename.rfind('.')
        vid = trans_filename[:dot_pos]
        trans_path = os.path.join(trans_dir, trans_filename)
        with open(trans_path) as f:
            trans_info = json.load(f)

        result[vid] = []
        for sentence_info in trans_info:
            for word_info in sentence_info['words']:
                ms = (word_info['start'] + word_info['end']) / 2 * 1000
                result[vid].append([ms, word_info['word']])
    with open(output_path, 'w') as f:
        json.dump(result, f)
    return result


def main():
    parser = argparse.ArgumentParser(description='Process transcripts to prepare for extracting frames')
    parser.add_argument('input', help='directory of transcripts to process')
    parser.add_argument('-o', '--output', default='output.json', help='path of output json file')
    args = parser.parse_args()
    process_transcript(args.input, args.output)


if __name__ == '__main__':
    main()

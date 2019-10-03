#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import cv2
import json
import matplotlib.pyplot as plt
import os
import pickle


def extract_frame(trans_dir, video_dir, frame_dir=None, data_path='data', append=False):
    trans_type = 'json'
    frame_type = 'png'
    if frame_dir and not os.path.isdir(frame_dir):
        os.makedirs(frame_dir)
    data_dir = os.path.dirname(data_path)
    if append and os.path.isfile(data_path):
        with open(data_path, 'rb') as f:
            image_text_pairs = pickle.load(f)
    else:
        image_text_pairs = []
        if data_dir and not os.path.isdir(data_dir):
            os.makedirs(data_dir)

    for video_filename in os.listdir(video_dir):
        video_path = os.path.join(video_dir, video_filename)
        if not os.path.isfile(video_path):
            continue
        dot_pos = video_filename.rfind('.')
        trans_filename_without_postfix = video_filename[:dot_pos] if dot_pos != -1 else video_filename
        trans_filename = trans_filename_without_postfix + '.' + trans_type
        trans_path = os.path.join(trans_dir, trans_filename)
        if not os.path.isfile(trans_path):
            continue
        print('Now processing: ' + trans_filename)
        with open(trans_path) as f:
            trans_info = json.load(f)
        capture = cv2.VideoCapture(video_path)

        for sentence_info in trans_info:
            for word_info in sentence_info['words']:
                ms = (word_info['start'] + word_info['end']) / 2 * 1000
                capture.set(cv2.CAP_PROP_POS_MSEC, ms)
                ms = capture.get(cv2.CAP_PROP_POS_MSEC)
                frame = capture.read()[1]
                image_text_pairs.append((frame, word_info['word']))
                if not frame_dir:
                    continue
                cleaned_word = ''.join(c if c.isalnum() else '-' for c in word_info['word'])
                frame_filename = '_'.join([trans_filename_without_postfix, str(round(ms)), cleaned_word]) + \
                                 '.' + frame_type
                frame_path = os.path.join(frame_dir, frame_filename)
                plt.imsave(frame_path, frame)
        capture.release()
    with open(data_path, 'wb') as f:
        pickle.dump(image_text_pairs, f)


def main():
    parser = argparse.ArgumentParser(description='Extract frames from videos and transcripts')
    parser.add_argument('trans_dir', help='directory of transcripts to process')
    parser.add_argument('video_dir', help='directory of videos to process')
    parser.add_argument('-o', '--output', help='directory of frames to output')
    parser.add_argument('-d', '--data', default='data', help='path of output data')
    parser.add_argument('-a', '--append', action='store_true', help='whether to append to existing results')
    args = parser.parse_args()
    extract_frame(args.trans_dir, args.video_dir, args.output, args.data, args.append)


if __name__ == '__main__':
    main()

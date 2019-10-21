#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import cv2
import json
import matplotlib.pyplot as plt
import os
import pickle


def extract_frame(trans_path, video_dir, frame_dir=None, data_path='data', append=False):
    frame_type = 'png'
    with open(trans_path) as f:
        trans_info = json.load(f)
    if frame_dir and not os.path.isdir(frame_dir):
        os.makedirs(frame_dir)
    data_dir = os.path.dirname(data_path)
    if append and os.path.isfile(data_path):
        with open(data_path, 'rb') as f:
            image_text_pairs = pickle.load(f)
    else:
        image_text_pairs = {}
        if data_dir and not os.path.isdir(data_dir):
            os.makedirs(data_dir)

    for video_filename in os.listdir(video_dir):
        video_path = os.path.join(video_dir, video_filename)
        if not os.path.isfile(video_path):
            continue
        dot_pos = video_filename.rfind('.')
        trans_filename_without_postfix = video_filename[:dot_pos] if dot_pos != -1 else video_filename
        if trans_filename_without_postfix not in trans_info:
            continue
        print('Now processing: ' + video_filename)
        capture = cv2.VideoCapture(video_path)

        for ms, text in trans_info[trans_filename_without_postfix]:
            capture.set(cv2.CAP_PROP_POS_MSEC, ms)
            ms = capture.get(cv2.CAP_PROP_POS_MSEC)
            frame = capture.read()[1]
            image_text_pairs[trans_filename_without_postfix, round(ms)] = frame, text
            if not frame_dir:
                continue
            cleaned_word = ''.join(c.lower() if c.isalnum() else '-' for c in text)
            frame_filename = '_'.join([trans_filename_without_postfix, str(round(ms)), cleaned_word]) + \
                             '.' + frame_type
            frame_path = os.path.join(frame_dir, frame_filename)
            plt.imsave(frame_path, frame)
        capture.release()
    with open(data_path, 'wb') as f:
        pickle.dump(image_text_pairs, f)
    return image_text_pairs


def main():
    parser = argparse.ArgumentParser(description='Extract frames from processed transcript and videos')
    parser.add_argument('input', help='path of processed transcript file')
    parser.add_argument('video_dir', help='directory of videos to process')
    parser.add_argument('-o', '--output', help='directory of frames to output')
    parser.add_argument('-d', '--data', default='data', help='path of output data')
    parser.add_argument('-a', '--append', action='store_true', help='whether to append to existing results')
    args = parser.parse_args()
    extract_frame(args.input, args.video_dir, args.output, args.data, args.append)


if __name__ == '__main__':
    main()

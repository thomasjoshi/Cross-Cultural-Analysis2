#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import cv2
import json
import matplotlib.pyplot as plt
import os
import pickle
import sys

src = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(src, 'dataset'))
sys.path.insert(0, os.path.join(src, 'spidering'))
from download import download
from extract_feature import get_image_features
from find_duplicate import get_duplicates
from get_metadata import get_metadata


def sample_frames(input_dir, output_dir, num_frames, no_frames):
    frame_type = 'png'
    text = ''
    if not no_frames and not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    image_text_pairs = {}
    for video_filename in os.listdir(input_dir):
        video_path = os.path.join(input_dir, video_filename)
        if not (os.path.isfile(video_path) and (video_filename.endswith('.mp4') or video_filename.endswith('.flv'))):
            continue
        dot_pos = video_filename.rfind('.')
        vid = video_filename[:dot_pos]
        capture = cv2.VideoCapture(video_path)
        frame_quantity = capture.get(cv2.CAP_PROP_FRAME_COUNT)
        for i in range(num_frames):
            ratio = (i + 1) / (num_frames + 1)
            capture.set(cv2.CAP_PROP_POS_FRAMES, ratio * frame_quantity)
            ms = round(capture.get(cv2.CAP_PROP_POS_MSEC))
            frame = capture.read()[1]
            frame_filename = f'{vid}_{ms}.{frame_type}'
            image_text_pairs[vid, ms] = frame, text
            if not no_frames:
                frame_path = os.path.join(output_dir, frame_filename)
                plt.imsave(frame_path, frame)
        capture.release()
    if not no_frames:
        with open(os.path.join(output_dir, 'data'), 'wb') as f:
            pickle.dump(image_text_pairs, f)
    return image_text_pairs


def process_topic(topic_cn, topic_en, key, output_dir, threshold, distance, video_quantity, num_frames, no_download,
                  no_frames):
    topic_en_cleaned = ''.join(c.lower() if c.isalnum() else '-' for c in topic_en)
    topic_dir = os.path.join(output_dir, topic_en_cleaned)
    chinese_dir = os.path.join(topic_dir, 'chinese')
    english_dir = os.path.join(topic_dir, 'english')
    chinese_metadata_dir = os.path.join(chinese_dir, 'metadata')
    english_metadata_dir = os.path.join(english_dir, 'metadata')
    chinese_videos_dir = os.path.join(chinese_dir, 'videos')
    english_videos_dir = os.path.join(english_dir, 'videos')
    chinese_frames_dir = os.path.join(chinese_dir, 'frames')
    english_frames_dir = os.path.join(english_dir, 'frames')
    chinese_features_path = os.path.join(chinese_frames_dir, 'features')
    english_features_path = os.path.join(english_frames_dir, 'features')
    sources_cn = ['bilibili', 'qq', 'iqiyi']
    sources_en = ['youtube']

    if no_download:
        with open(chinese_features_path, 'rb') as f:
            features_cn = pickle.load(f)
        with open(english_features_path, 'rb') as f:
            features_en = pickle.load(f)
    else:
        for i, source in enumerate(sources_cn):
            num = video_quantity // len(sources_cn) + (i < video_quantity % len(sources_cn))
            get_metadata(topic_cn, quantity=num, output=chinese_metadata_dir, append=True, key=key, sources=(source,))
        for i, source in enumerate(sources_en):
            num = video_quantity // len(sources_en) + (i < video_quantity % len(sources_en))
            get_metadata(topic_en, quantity=num, output=english_metadata_dir, append=True, key=key, sources=(source,))
        download(os.path.join(chinese_metadata_dir, 'metadata'), output=chinese_videos_dir)
        download(os.path.join(english_metadata_dir, 'metadata'), output=english_videos_dir)
        image_text_pairs_cn = sample_frames(chinese_videos_dir, chinese_frames_dir, num_frames, no_frames)
        image_text_pairs_en = sample_frames(english_videos_dir, english_frames_dir, num_frames, no_frames)
        features_cn = get_image_features(image_text_pairs_cn)
        features_en = get_image_features(image_text_pairs_en)
        if not os.path.isdir(chinese_frames_dir):
            os.makedirs(chinese_frames_dir)
        with open(chinese_features_path, 'wb') as f:
            pickle.dump(features_cn, f)
        if not os.path.isdir(english_frames_dir):
            os.makedirs(english_frames_dir)
        with open(english_features_path, 'wb') as f:
            pickle.dump(features_en, f)

    duplicate_pairs = get_duplicates(features_cn, features_en, threshold, distance)
    if not os.path.isdir(topic_dir):
        os.makedirs(topic_dir)
    with open(os.path.join(topic_dir, 'pairs.json'), 'w') as f:
        json.dump(duplicate_pairs, f)
    return duplicate_pairs


def find_topics(chinese_topics, english_topics, key, output='output', threshold=0.25, distance='angular',
                video_quantity=3, num_frames=10, no_download=False, no_frames=False):
    with open(chinese_topics) as f:
        cn = f.read().splitlines()
    with open(english_topics) as f:
        en = f.read().splitlines()
    counts = []
    for topic_cn, topic_en in zip(cn, en):
        pairs = process_topic(topic_cn, topic_en, key, output, threshold, distance, video_quantity, num_frames,
                              no_download, no_frames)
        counts.append(len(pairs))
    plt.bar(en, counts)
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Sample videos for topics and find similar frames')
    parser.add_argument('chinese', help='chinese topics file')
    parser.add_argument('english', help='english topics file')
    parser.add_argument('key', help='key for Youtube API, string or path to text file')
    parser.add_argument('-o', '--output', default='output', help='output directory')
    parser.add_argument('-t', '--threshold', type=float, default=0.25, help='threshold of similarity')
    parser.add_argument('-d', '--distance', default='angular', help='distance function, can be l1, l2, angular')
    parser.add_argument('-n', '--quantity', type=int, default=3,
                        help='number of videos to sample per language per topic')
    parser.add_argument('-f', '--num-frames', type=int, default=10, help='number of frames to sample per video')
    parser.add_argument('--no-download', action='store_true', help='use existing videos if set')
    parser.add_argument('--no-frames', action='store_true', help='do not store frames if set')
    args = parser.parse_args()
    find_topics(args.chinese, args.english, args.key, args.output, args.threshold, args.distance, args.quantity,
                args.num_frames, args.no_download, args.no_frames)


if __name__ == '__main__':
    main()

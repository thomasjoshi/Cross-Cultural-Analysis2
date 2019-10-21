#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import json
import numpy as np
import os
import pickle


def l1(a, b):
    return np.sum(np.abs(a - b)).item()


def l2(a, b):
    return np.sqrt(np.sum((a - b) ** 2)).item()


def angular_dist(a, b):
    cos = a @ b / np.sqrt(np.sum(a ** 2) * np.sum(b ** 2))
    if cos < -1:
        cos = -1
    if cos > 1:
        cos = 1
    return np.arccos(cos) / np.pi


def get_duplicates(features_cn, features_en, threshold, distance):
    distance = distance.lower()
    if distance.startswith('l1'):
        dist_func = l1
    elif distance.startswith('l2'):
        dist_func = l2
    else:
        dist_func = angular_dist
    pairs = []
    for (vid_cn, ms_cn), (image_cn, text_cn) in features_cn.items():
        for (vid_en, ms_en), (image_en, text_en) in features_en.items():
            d = dist_func(image_cn, image_en)
            if d < threshold:
                pairs.append([vid_cn, ms_cn, vid_en, ms_en, d])
    pairs.sort(key=lambda x: x[-1])
    return pairs


def find_duplicate(features_path_cn, features_path_en, output_path='output.json', threshold=0.25, distance='angular'):
    with open(features_path_cn, 'rb') as f:
        features_cn = pickle.load(f)
    with open(features_path_en, 'rb') as f:
        features_en = pickle.load(f)
    pairs = get_duplicates(features_cn, features_en, threshold, distance)
    output_dir = os.path.dirname(output_path)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    with open(output_path, 'w') as f:
        json.dump(pairs, f)
    return pairs


def main():
    parser = argparse.ArgumentParser(description='Find nearly duplicate frames from extracted features')
    parser.add_argument('input_cn', help='path to chinese features data file')
    parser.add_argument('input_en', help='path to english features data file')
    parser.add_argument('-o', '--output', default='output.json', help='path to output json file')
    parser.add_argument('-t', '--threshold', type=float, default=0.25, help='threshold of similarity')
    parser.add_argument('-d', '--distance', default='angular', help='distance function, can be l1, l2, angular')
    args = parser.parse_args()
    find_duplicate(args.input_cn, args.input_en, args.output, args.threshold, args.distance)


if __name__ == '__main__':
    main()

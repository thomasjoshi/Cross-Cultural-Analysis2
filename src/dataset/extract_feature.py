#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import tensorflow as tf
from tensorflow import keras


#tf.config.experimental.set_memory_growth(tf.config.experimental.list_physical_devices('GPU')[0], True)


class Extractor:
    def __init__(self):
        vgg19 = keras.applications.vgg19.VGG19()
        self.model = keras.models.Sequential()
        for layer in vgg19.layers[:-1]:
            self.model.add(layer)

    def extract_frames(self, frames):
        features = self.model.predict(frames, batch_size=16)
        return features


def get_image_features(image_text_pairs):
    shape = (224, 224)
    keys = list(image_text_pairs.keys())
    frames = (np.stack([cv2.resize(image_text_pairs[k][0], shape) for k in keys]) / 255).astype(np.float32)
    texts = [image_text_pairs[k][1] for k in keys]
    extractor = Extractor()
    features = list(extractor.extract_frames(frames))
    result = {k: (feature, text) for k, feature, text in zip(keys, features, texts)}
    return result


def extract_feature(input_frames, output_path='output'):
    frame_type = 'png'
    if not os.path.exists(input_frames):
        raise FileNotFoundError(f'No such file or directory: {input_frames}')
    if os.path.isfile(input_frames):
        with open(input_frames, 'rb') as f:
            image_text_pairs = pickle.load(f)
    else:
        image_text_pairs = {}
        for frame_filename in os.listdir(input_frames):
            if not frame_filename.endswith('.' + frame_type):
                continue
            dot_pos = frame_filename.rfind('.')
            frame_filename_without_postfix = frame_filename[:dot_pos]
            info = frame_filename_without_postfix.split('_')
            if len(info) == 1:
                vid = info
                ms = '0'
                text = ''
            elif len(info) == 2:
                vid, ms = info
                text = ''
            elif len(info) == 3:
                vid, ms, text = info
            else:
                continue
            ms = int(ms)
            frame_path = os.path.join(input_frames, frame_filename)
            frame = plt.imread(frame_path)
            if frame.shape[-1] > 3:
                frame = frame.T[:3].T
            frame *= 255
            image_text_pairs[(vid, ms)] = frame, text
    result = get_image_features(image_text_pairs)
    output_dir = os.path.dirname(output_path)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    with open(output_path, 'wb') as f:
        pickle.dump(result, f)
    return result


def main():
    parser = argparse.ArgumentParser(description='Extract features from image and text pairs')
    parser.add_argument('input', help='directory of frames or path to pairs data file')
    parser.add_argument('-o', '--output', default='output', help='path to output data file')
    args = parser.parse_args()
    extract_feature(args.input, args.output)


if __name__ == '__main__':
    main()

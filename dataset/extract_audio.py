#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract audios from videos')
    parser.add_argument('input', help='directory of videos to process')
    parser.add_argument('-o', '--output', default='audios', help='directory of audios to output')
    parser.add_argument('-f', '--audio-format', default='flac', help='output audios format')
    parser.add_argument('-r', '--sampling-rate', type=int, default=16000, help='sampling rate of ffmpeg')
    parser.add_argument('-c', '--audio-channel', type=int, default=1, help='default is mono channel')
    args = parser.parse_args()

    video_dir = args.input
    audio_dir = args.output
    audio_type = args.audio_format
    sampling_rate = args.sampling_rate
    audio_channel = args.audio_channel

    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    for video_filename in os.listdir(video_dir):
        video_path = os.path.join(video_dir, video_filename)
        if not os.path.isfile(video_path):
            continue
        dot_pos = video_filename.rfind('.')
        audio_filename = (video_filename[:dot_pos] if dot_pos != -1 else video_filename) + '.' + audio_type
        audio_path = os.path.join(audio_dir, audio_filename)
        os.system('ffmpeg -y -i ' + video_path + ' -f ' + audio_type + ' -r ' + str(sampling_rate) + ' -ac ' + str(
            audio_channel) + ' ' + audio_path)

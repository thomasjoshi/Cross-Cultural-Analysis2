#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import os
from spider import Spider


# def download(input_file, output='output', sources=None):
#     if not os.path.isdir(output):
#         os.makedirs(output)
#     spider = Spider()
#     spider.load(input_file)
#     spider.download(output, sources)
def download(input_file, audio_output='audio_output', video_output='video_output', sources=None):
    if not os.path.isdir(video_output):
        os.makedirs(video_output)
    if not os.path.isdir(audio_output):
        os.makedirs(audio_output)
    spider = Spider()
    spider.load(input_file)
    spider.download(audio_output, video_output, sources)    


def main():
    # parser = argparse.ArgumentParser(description='download videos using metadata')
    # parser.add_argument('input', help='input metadata file')
    # parser.add_argument('-o', '--output', default='output', help='output directory')
    # parser.add_argument('-s', '--sources', nargs='*', help='filter sources')
    # args = parser.parse_args()
    # download(args.input, args.output, args.sources)
    parser = argparse.ArgumentParser(description='download videos using metadata')
    parser.add_argument('input', help='input metadata file')
    parser.add_argument('-ao', '--audio_output', default='audios', help='audio output directory')
    parser.add_argument('-vo', '--video_output', default='videos', help='video output directory')
    parser.add_argument('-s', '--sources', nargs='*', help='filter sources')
    args = parser.parse_args()
    download(args.input, args.audio_output, args.video_output, args.sources)

 
if __name__ == '__main__':
    main()

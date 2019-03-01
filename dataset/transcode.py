#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import argparse
from os import walk
from shutil import copyfile

parser = argparse.ArgumentParser(description='Transcode: process RAW vieo file from spider')
parser.add_argument('--rename', type=int, default=1, help='rename the raw file')
parser.add_argument('--split', type=int, default=1, help='split audio file from video file')
parser.add_argument('--folder', type=str, default="english", help='sub folder in dataset')
parser.add_argument('--dataset', type=str, default="AlphaGo", help='name of the news event')
parser.add_argument('--video_format', type=str, default=".mp4", help='format of input videos')
parser.add_argument('--audio_format', type=str, default=".flac", help='format of output audios')
parser.add_argument('--sampling_rate', type=int, default=16000, help='sampling rate of ffmpeg')
parser.add_argument('--audio_channel', type=int, default=1, help='default is mono channel')
opt = parser.parse_args()

def replace(parent):
    for path, folders, files in os.walk(parent):
        for f in files:
            os.rename(os.path.join(path, f), os.path.join(path, f.replace(' ', '_')))
        for i in range(len(folders)):
            new_name = folders[i].replace(' ', '_')
            os.rename(os.path.join(path, folders[i]), os.path.join(path, new_name))
            folders[i] = new_name

dataset_name = "./" + opt.dataset
dataset_path = dataset_name + "/" + opt.folder
raw_path = dataset_path + "/raws"
video_path = dataset_path + "/videos"
audio_path = dataset_path + "/audios"
tran_path = dataset_path + "/transcripts"

video_type = opt.video_format
audio_type = opt.audio_format

if not os.path.exists(raw_path):
    print('Error: no file in the raw folder.')

if not os.path.exists(video_path):
    os.makedirs(video_path)

if not os.path.exists(audio_path):
    os.makedirs(audio_path)

if not os.path.exists(trans_path):
    os.makedirs(trans_path)

if opt.rename:
    replace(raw_path)

    r_list = []

    for (dirpath, dirnames, filenames) in walk(raw_path):
        r_list.extend(filenames)

    count = 1
    for index,raw_filename in enumerate(r_list):
        if raw_filename[-len(video_type):] == video_type and raw_filename[0] != '.':
            audio_filename = audio_path + '/' + str(count) + audio_type
            video_filename = video_path + '/' + str(count) + video_type
            copyfile(raw_path+'/'+raw_filename, video_filename)
            count += 1

if opt.split:
    n_list = []
    for (dirpath, dirnames, filenames) in walk(video_path):
        n_list.extend(filenames)

    for index,video_filename in enumerate(n_list):
        cmd = ' '
        audio_filename = audio_path + '/' + video_filename[:-len(video_type)] + audio_type
        try:
            os.system(cmd.join(('ffmpeg -y -i',video_path + '/' + video_filename, '-f flac -r ',str(opt.sampling_rate),' -ac ',str(opt.audio_channel), audio_filename)))
        except Exception as e:
            os.remove(video_path + '/' + video_filename)
            print("===> file corrupted, automatically remove...")

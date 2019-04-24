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

dataset_name = "./" + opt.dataset
dataset_path = dataset_name + "/" + opt.folder
raw_path_video = dataset_path + "/source/videos"
raw_path_description = dataset_path + "/source/descriptions"
description_path = dataset_path + "/descriptions"
video_path = dataset_path + "/videos"
audio_path = dataset_path + "/audios"
trans_path = dataset_path + "/transcripts"

video_type = opt.video_format
audio_type = opt.audio_format

if not os.path.exists(raw_path_video):
    print('Error: no file in the raw folder.')

if not os.path.exists(raw_path_description):
    print('Error: no file in the raw folder.')

if not os.path.exists(video_path):
    os.makedirs(video_path)

if not os.path.exists(description_path):
    os.makedirs(description_path)

if not os.path.exists(audio_path):
    os.makedirs(audio_path)

if not os.path.exists(trans_path):
    os.makedirs(trans_path)

if opt.rename:

    r_list = []
    d_list = []

    for (dirpath, dirnames, filenames) in walk(raw_path_video):
        r_list.extend(filenames)

    for (dirpath, dirnames, filenames) in walk(raw_path_description):
        d_list.extend(filenames)


    count = 1
    for index,raw_filename in enumerate(r_list):
        if raw_filename[-len(video_type):] == video_type and raw_filename[0] != '.':
            #audio_filename = audio_path + '/' + str(count) + audio_type
            video_filename = video_path + '/' + str(count) + video_type

            video_file_num  = raw_filename[:raw_filename.find('_')]

            for idx,description_filename in enumerate(d_list):
                des_file_num = description_filename[:description_filename.find('_')]

                #print(title1, title2)
                if video_file_num == des_file_num:
                    desription_ori = raw_path_description + '/' + description_filename
                    description_dst = description_path + '/' + str(count) + '.txt'
                    copyfile(raw_path_video+'/'+raw_filename, video_filename)
                    copyfile(desription_ori, description_dst)
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

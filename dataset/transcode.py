import os
from os import walk

dataset_name = "./AlphaGo"
dataset_path = dataset_name + "/english"
raw_path = dataset_path + "/raws"
video_path = dataset_path + "/videos"
audio_path = dataset_path + "/audios"
transcript_path = dataset_path + "/transcripts"

video_type = '.mp4'

if not os.path.exists(raw_path):
    print('Error: no file in the raw folder.')

if not os.path.exists(video_path):
    os.makedirs(video_path)

if not os.path.exists(audio_path):
    os.makedirs(audio_path)

if not os.path.exists(transcript_path):
    os.makedirs(transcript_path)

r_list = []

for (dirpath, dirnames, filenames) in walk(raw_path):
    r_list.extend(filenames)

count = 1
for index,raw_filename in enumerate(r_list):
    if raw_filename[-4:] == video_type:
        cmd = ' '
        audio_filename = audio_path + '/' + str(count) + '.mp3'
        video_filename = video_path + '/' + str(count) + video_type
        os.rename(raw_path+'/'+raw_filename, video_filename)
        #os.system(cmd.join(('cp',raw_path+'/'+raw_filename, video_path)))
        #os.system(cmd.join(('mv',video_path+'/'+raw_filename, video_filename)))
    	os.system(cmd.join(('ffmpeg -i',video_filename, '-f mp3 -ab 192000 -vn', audio_filename)))
        count += 1

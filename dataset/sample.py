import cv2
import math
import os
import argparse
from os import walk
import numpy as np

parser = argparse.ArgumentParser(description='extract_frame: extract frames and words')
parser.add_argument('--folder', type=str, default="english", help='sub folder in dataset')
parser.add_argument('--dataset', type=str, default="AlphaGo", help='name of the news event')
parser.add_argument('--video_format', type=str, default=".mp4", help='format of input videos')
parser.add_argument('--transcript_format', type=str, default=".txt", help='format of output audios')
parser.add_argument('--interval', type=int, default=5, help='length of sampling interval')
parser.add_argument('--threshold', type=float, default=150, help='treshold of inter frame differences')
opt = parser.parse_args()

dataset_name = "./" + opt.dataset
dataset_path = dataset_name + "/" + opt.folder
video_path = dataset_path + "/videos"
trans_path = dataset_path + "/transcripts"
out_frame_path = dataset_path + "/frames"
out_text_path = dataset_path + "/texts"

video_type = opt.video_format

if not os.path.exists(trans_path):
    print('Error: no file in the transcript folder.')

if not os.path.exists(out_frame_path):
    os.makedirs(out_frame_path)

if not os.path.exists(out_text_path):
    os.makedirs(out_text_path)

# read all file in the video path
f_list = []
for (dirpath, dirnames, filenames) in walk(trans_path):
    f_list.extend(filenames)

sample_interval = opt.interval

for index,trans_file in enumerate(f_list):
    print(u'Now processing: {}'.format(trans_file))
    samples = []
    start_time = []
    end_time = []
    word_buffer = []

    video_file = trans_file[:-len(opt.transcript_format)] + video_type
    full_video_path = video_path + "/" + video_file
    full_trans_path = trans_path + "/" + trans_file
    if(os.path.isfile(full_trans_path)):
        fp = open(full_trans_path)
        lines = fp.read().split("\n")
        for line in lines:
            words = line.split('\t')
            if len(words) == 4:
                word_buffer.append(words[0])
                start_time.append(float(words[1]))
                end_time.append(float(words[2]))
                #confidence.append(float(words[3]))

        traverse_index = 0
        old_traverse_index = traverse_index

        while traverse_index < len(word_buffer):
            sample_words = ""
            is_jump = False
            t1 = start_time[traverse_index]
            t2 = end_time[traverse_index]

            while(traverse_index < len(word_buffer) and end_time[traverse_index] - t1 < sample_interval):
                is_jump = True
                sample_words += word_buffer[traverse_index]
                t2 = end_time[traverse_index]
                traverse_index += 1

            if is_jump == True:
                is_jump = False
                traverse_index = old_traverse_index + int(opt.interval)

            traverse_index += 1 # arbitrarily skip n words
            old_traverse_index = traverse_index

            samples.append([t1,t2,sample_words])

        print("===> Total number of interval: " + str(len(samples)))

        '''
        for sample in samples:
            print(sample[2].decode('utf-8').encode('utf-8'))
        exit()
        '''

        capture = cv2.VideoCapture(full_video_path)
        frameRate = capture.get(5) # get frame rate

        idx = 0
        count = 0
        is_ready = True
        last_frame = -1

        while(capture.isOpened() and idx < len(samples)):
            frameId = capture.get(1)
            ret, frame = capture.read()

            if frameId == last_frame:
                break
            else:
                last_frame = frameId

            if (frameId <= samples[idx][1] * frameRate and frameId >= samples[idx][0] * frameRate):
                is_ready = False
                if frameId % round(frameRate) == 0:
                #if np.sum( np.absolute(frame-last_frame) )/np.size(frame) > opt.threshold:
                    out_filename = '_'.join([str(int(samples[idx][0])),str(int(samples[idx][1]))])
                    out_img_filename = out_frame_path + "/" + trans_file[:-len(opt.transcript_format)] + "/" + out_filename + "_" + str(count) + ".jpg"
                    if not os.path.exists(out_frame_path + "/" + trans_file[:-len(opt.transcript_format)]):
                        os.makedirs(out_frame_path + "/" + trans_file[:-len(opt.transcript_format)])
                    cv2.imwrite(out_img_filename, frame)
                    count += 1
                    print("Writing frame: " + out_img_filename)

            if (not is_ready and frameId > samples[idx][1] * frameRate):
                try:
                    out_trans_filename = out_text_path + "/" + trans_file[:-len(opt.transcript_format)] + "/" + out_filename + ".txt"
                    if not os.path.exists(out_text_path + "/" + trans_file[:-len(opt.transcript_format)]):
                        os.makedirs(out_text_path + "/" + trans_file[:-len(opt.transcript_format)])
                    fw = open(out_trans_filename, 'w')
                    if opt.folder == "english":
                        fw.write(samples[idx][2]+'\n')
                    else:
                        fw.write(samples[idx][2].decode('utf-8').encode('utf-8')+'\n')
                    fw.close()
                except NameError:
                    print("No keyframe above threshold found...")

                count = 0
                is_ready = True

            while idx < len(samples) and frameId > samples[idx][0] * frameRate and is_ready:
                idx += 1

        capture.release()
        print ("Finish processing file: " + full_video_path)

    else:
        print("File connot find: " + full_trans_path)

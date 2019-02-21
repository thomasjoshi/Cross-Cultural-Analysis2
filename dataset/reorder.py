import math
import os
from os import walk
from pprint import pprint

dataset_path = "english"
video_path = dataset_path + "/videos"
trans_path = dataset_path + "/transcript"

# read all file in the video path
v_list = []
t_list = []

for (dirpath, dirnames, filenames) in walk(video_path):
    v_list.extend(filenames)

for (dirpath, dirnames, filenames) in walk(trans_path):
    t_list.extend(filenames)

count = 0
for index,video_filename in enumerate(v_list):
	underline_index = video_filename.find("_")
	query_filename = video_filename[underline_index+1:-7] + ".json"
	
	for idx,trans_filename in enumerate(t_list):
		underline_idx = trans_filename.find("_")
		result_filename = trans_filename[underline_idx+1:]
		#print(query_filename + "\n" + result_filename)
		if result_filename == query_filename:
			count += 1
			full_video_path = video_path + "/" + video_filename
			full_trans_path = trans_path + "/" + trans_filename
			os.rename(full_video_path, "./english/v/" + str(count) + "_" + query_filename[:-4] + "mp4")
			os.rename(full_trans_path, "./english/t/" + str(count) + "_" + query_filename)
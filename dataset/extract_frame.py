import cv2 
import math
import json
import os
from os import walk
from pprint import pprint

dataset_path = "AlphaGo"
video_path = dataset_path + "/videos"
trans_path = dataset_path + "/transcripts"
image_folder = dataset_path + "/images"

# read all file in the video path
f_list = []
for (dirpath, dirnames, filenames) in walk(video_path):
    f_list.extend(filenames)
f_list=["test.mp4"]

sample_interval = 3
start_sample_time = []
end_sample_time = []
start_time = []
end_time = []
words = []

for index,video_file in enumerate(f_list):
	trans_file = video_file[:-4] + ".json"
	full_video_path = video_path + "/" + video_file
	full_trans_path = trans_path + "/" + trans_file
	if(os.path.isfile(full_trans_path)):
		with open(full_trans_path) as trans_data:
			data = json.load(trans_data)
			for i in range(0, len(data)):
				words.append(str(data[i][0]))
				start_time.append(float(data[i][1]))
				end_time.append(float(data[i][2]))

			traverse_index = 0
			start = start_time[traverse_index]
			end = end_time[traverse_index]

			while(traverse_index < len(data)-1):
				if(end_time[traverse_index] - start >= sample_interval):
					if_end_exist = False
					if_start_exist = False
					try:
						if_start_exist = start_sample_time.index(start)
						if_end_exist = end_sample_time.index(end)
						start = start_time[traverse_index]
					except ValueError:
						if not if_end_exist and not if_start_exist:
							start_sample_time.append(start)
							end_sample_time.append(end)
							traverse_index += 1
							end = end_time[traverse_index]
							start = start_time[traverse_index]
							continue

				end = end_time[traverse_index]
				traverse_index += 1

		print("Total number of interval: " + str(len(start_sample_time)))
		#print(start_sample_time)

		count = 0
		capture = cv2.VideoCapture(full_video_path)
		frameRate = capture.get(5) # get frame rate
		
		while(capture.isOpened()):
		    frameId = capture.get(1) # current frame number
		    ret, frame = capture.read()
		    key_frame = math.floor((start_time[count] - float(start_time[count] - end_time[count])/2) * frameRate)
		    print(frameId,key_frame)
		    if (ret != True or count >= len(start_sample_time)):
		        break
		    if (frameId == key_frame):
		        filename = image_folder + "/" + str(count) + ".jpg"
		        cv2.imwrite(filename, frame)
		        print("Write frame: " + filename)
		        count += 1

		capture.release()
		print ("Finish processing file: " + full_video_path)

	else:
		print("File connot find: " + full_trans_path)

'''
with open('data.json') as f:
    data = json.load(f)
pprint(data)

video_file = "capture.avi"

cap = cv2.VideoCapture(videoFile)
frameRate = cap.get(5) #frame rate
while(cap.isOpened()):
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
    if (frameId % math.floor(frameRate) == 0):
        filename = imagesFolder + "/image_" +  str(int(frameId)) + ".jpg"
        cv2.imwrite(filename, frame)
cap.release()
print ("Finish Processing.")
'''
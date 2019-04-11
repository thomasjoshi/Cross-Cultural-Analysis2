#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import os
import time
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import walk
from collections import defaultdict

parser = argparse.ArgumentParser(description='extract_frame: extract frames and words')
parser.add_argument('--dataset', type=str, default="AlphaGo", help='name of the news event')
parser.add_argument('--feature_format', type=str, default=".npy", help='format of extracted visual features')
parser.add_argument('--threshold', type=float, default=0.1, help='threshold for picking near duplicate frames')
opt = parser.parse_args()

dataset_name = "./" + opt.dataset

chi_dataset_path = dataset_name + "/" + 'chinese'
chi_frame_path = chi_dataset_path + "/frames"
eng_dataset_path = dataset_name + "/" + 'english'
eng_frame_path = eng_dataset_path + "/frames"
out_path = dataset_name + "/near_duplicate"

if not os.path.exists(out_path):
    os.makedirs(out_path)

if not os.path.exists(out_path + '/chi'):
    os.makedirs(out_path + '/chi')

if not os.path.exists(out_path + '/eng'):
    os.makedirs(out_path + '/eng')

def find_similarity(A, B):
    mse = ((A - B)**2).mean(axis=0)
    return mse

def find_filename(full_path):
    tmp = full_path
    while tmp.find('/') >= 0:
        tmp = tmp[tmp.find('/')+1:]
    return tmp
#chi_frame_path = './test'
#eng_frame_path = './test'

# read all file in the frame path
f_list_chi = []
for dirpath, subdirs, files in os.walk(chi_frame_path):
    for x in files:
        if x.endswith(".npy"):
            f_list_chi.append(os.path.join(dirpath, x))

f_list_eng = []
for dirpath, subdirs, files in os.walk(eng_frame_path):
    for x in files:
        if x.endswith(".npy"):
            f_list_eng.append(os.path.join(dirpath, x))

count = 0
start = time.time()
with open(out_path+'/record.txt','w+') as f:
    for idx_chi, filename_chi in enumerate(f_list_chi):
        print(u'Now processing: {}'.format(filename_chi))
        feature_chi = np.load(filename_chi)
        for idxeng, filename_eng in enumerate(f_list_eng):
            feature_eng = np.load(filename_eng)

            l2_sim = find_similarity(feature_chi,feature_eng)

            if l2_sim < opt.threshold:
                count += 1
                img_chi = mpimg.imread(filename_chi[:-4]+'.jpg')
                img_eng = mpimg.imread(filename_eng[:-4]+'.jpg')

                '''
                f = plt.figure()
                f.add_subplot(1,2, 1)
                plt.imshow(img_chi)
                f.add_subplot(1,2, 2)
                plt.imshow(img_eng)
                plt.show(block=True)


                save_img_chi = find_filename(filename_chi)
                save_img_chi = out_path + '/chi/' + save_img_chi[:save_img_chi.rfind('_')] + '.jpg'

                save_img_eng = find_filename(filename_eng)
                save_img_eng = out_path + '/eng/' + save_img_eng[:save_img_eng.rfind('_')] + '.jpg'
                '''

                save_img_chi = out_path + '/chi/' + str(count) + '.jpg'
                save_img_eng = out_path + '/eng/' + str(count) + '.jpg'

                text_chi = filename_chi.replace('frames','texts')[:-4]
                text_chi = text_chi[:text_chi.rfind('_')] + '.txt'

                text_eng = filename_eng.replace('frames','texts')[:-4]
                text_eng = text_eng[:text_eng.rfind('_')] + '.txt'

                '''
                save_text_chi = save_img_chi.replace('frames','texts')[:-4] + '.txt'
                save_text_eng = save_img_eng.replace('frames','texts')[:-4] + '.txt'
                '''

                save_text_chi = out_path + '/chi/' + str(count) + '.txt'
                save_text_eng = out_path + '/eng/' + str(count) + '.txt'

                os.system(' '.join(['cp', filename_chi[:-4]+'.jpg', save_img_chi]))
                os.system(' '.join(['cp', filename_eng[:-4]+'.jpg', save_img_eng]))

                os.system(' '.join(['cp', text_chi, save_text_chi]))
                os.system(' '.join(['cp', text_eng, save_text_eng]))

                f.write(filename_chi[:-4]+'.jpg'+'->'+save_img_chi+'\n')
                f.write(filename_eng[:-4]+'.jpg'+'->'+save_img_eng+'\n')
                f.write(text_chi+'->'+save_text_chi+'\n')
                f.write(text_eng+'->'+save_text_eng+'\n')
                f.write('\n')

end = time.time()
print('Total time: ' + str(round(end-start,3)) + ' seconds.')

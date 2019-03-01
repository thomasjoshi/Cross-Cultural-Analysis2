#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import jieba
import argparse
from os import walk
from google.cloud import translate

parser = argparse.ArgumentParser(description='Translate Analysis: Simple code to see the effect of binlingual translation')
parser.add_argument('--dataset', type=str, default="AlphaGo", help='name of the news event')
opt = parser.parse_args()

translate_client = translate.Client()

dataset_name = "./" + opt.dataset
chinese_dataset_path = dataset_name + "/" + 'chinese'
english_dataset_path = dataset_name + "/" + 'english'
out_path = dataset_name + "/" + 'misc'

chinese_trans_path = chinese_dataset_path + "/transcripts"
english_trans_path = english_dataset_path + "/transcripts"

if not os.path.exists(chinese_trans_path) or not os.path.exists(english_trans_path):
    print("Error: there is no transcript available for analysis...")

chi_list = []
for (dirpath, dirnames, filenames) in walk(chinese_trans_path):
    chi_list.extend(filenames)

eng_list = []
for (dirpath, dirnames, filenames) in walk(english_trans_path):
    eng_list.extend(filenames)

chinese_words = []
chi2eng_words = []
english_words = []

for index,trans_file in enumerate(chi_list):
    full_trans_path = chinese_trans_path + "/" + trans_file
    if(os.path.isfile(full_trans_path)):
        fp = open(full_trans_path)
        lines = fp.read().split("\n")
        for line in lines:
            words = line.split('\t')
            if len(words) == 2:
                seg_list = list(jieba.cut(words[0], cut_all=False))
                for text in seg_list:
                    translation = translate_client.translate(
                        text,
                        source_language='zh-CN',
                        target_language='en')

                    print(u'{}->{}'.format(text,translation['translatedText']))
                    chinese_words.append(u''.format(text))
                    chi2eng_words.append(u''.format(translation['translatedText']))

for index,trans_file in enumerate(eng_list):
    full_trans_path = english_trans_path + "/" + trans_file
    if(os.path.isfile(full_trans_path)):
        fp = open(full_trans_path)
        lines = fp.read().split("\n")
        for line in lines:
            words = line.split('\t')
            if len(words) == 4:
                english_words.append(words[0])

chi2eng_log = open(out_path + 'chi2eng.txt', 'w')
english_log = open(out_path + 'english.txt', 'w')
common_log = open(out_path + 'common.txt', 'w')
unique_log = open(out_path + 'unique.txt', 'w')

for i in range(len(chi2eng_words)):
    chi2eng_log.write(chi2eng_words[i] + '\t' + chinese_words[i].encode('utf-8') + '\n')

for i in range(len(english_words)):
    english_words.write(english_words[i] + '\n')

print(len(chi2eng_words))
print(len(english_words))

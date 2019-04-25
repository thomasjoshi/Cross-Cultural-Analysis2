#!/usr/bin/python
# -*- coding: UTF-8 -*-

import math
import os
import re
import collections
import jieba
import argparse
from os import walk
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from collections import Counter
import matplotlib.pylab as plt
import matplotlib
import io
import codecs

lemmatizer = WordNetLemmatizer()

matplotlib.rc('font', **{'sans-serif' : 'Arial',
                         'family' : 'sans-serif'})

parser = argparse.ArgumentParser(description='extract_frame: extract frames and words')
parser.add_argument('--folder', type=str, default="english", help='sub folder in dataset')
parser.add_argument('--dataset', type=str, default="AlphaGo", help='name of the news event')
parser.add_argument('--video_format', type=str, default=".mp4", help='format of input videos')
parser.add_argument('--transcript_format', type=str, default=".txt", help='format of output audios')
parser.add_argument('--top_k', type=int, default=100, help='top words from blacklist of whitelist')
parser.add_argument('--threshold', type=int, default=20, help='treshold for filtering out the videos')
parser.add_argument('--blacklist', type=str, default='blacklist.txt', help='relative path for blacklist')
parser.add_argument('--whitelist', type=str, default='whitelist.txt', help='relative path for whitelist')
opt = parser.parse_args()
print(opt)

dataset_name = "./" + opt.dataset
dataset_path = dataset_name + "/" + opt.folder
video_path = dataset_path + "/videos"
trans_path = dataset_path + "/transcripts"
blacklist_path = dataset_path + '/' +  opt.blacklist
whitelist_path = dataset_path + '/' +  opt.whitelist

def Diff(li1, li2):
    return (list(set(li1) - set(li2)))

blacklist_dict = {}
with codecs.open(blacklist_path, encoding='utf-8') as fr:
    lines = fr.read().splitlines()

for index, line in enumerate(lines):
    contents = line.split()

    if len(contents) < 2:
        continue

    bl_word, freq = contents[0], int(contents[1])
    blacklist_dict[bl_word] = freq
    if index + 1 >= opt.top_k:
        break

whitelist_dict = {}
with codecs.open(whitelist_path, encoding='utf-8') as fr:
    lines = fr.read().splitlines()

for index, line in enumerate(lines):
    contents = line.split()

    if len(contents) < 2:
        continue

    bl_word, freq = contents[0], int(contents[1])
    whitelist_dict[bl_word] = freq
    if index + 1 >= opt.top_k:
        break

f_list = []
for (dirpath, dirnames, filenames) in walk(trans_path):
    f_list.extend(filenames)

ads_words = Counter()
freq_words = Counter()

for index, trans_file in enumerate(f_list):
    print(''.join(['===> Processing: ', trans_file]))
    with codecs.open('/'.join([trans_path, trans_file]), encoding='utf-8') as fr:
        lines = fr.read().splitlines()

    if len(lines) > 0:
        for line in lines:
            if len(line.split('\t')) == 2:
                if opt.folder == 'english':
                    remove_freq_list = lines[0].split()[:-2]
                    content = ' '.join(remove_freq_list)

                    text = nltk.word_tokenize(content)
                    lemmatized_text = []
                    for word in text:
                        lemmatized_text.append(lemmatizer.lemmatize(word))

                    #print(Diff(text,lemmatized_text))

                    tagged = nltk.pos_tag(lemmatized_text)
                    entities = nltk.chunk.ne_chunk(tagged)

                    '''
                    fdist = FreqDist(lemmatized_text)
                    tab = fdist.tabulate(10, cumulative=False)
                    fdist.plot(10, cumulative=False)
                    '''
                elif opt.folder == 'chinese':
                    content = line.split('\t')[0]
                    lemmatized_text = jieba.cut(content, cut_all=False)
                    #print(content.decode('utf-8').encode('utf-8'))
                else:
                    print('error: unacceptable folder name')

                for word in lemmatized_text:
                    freq_words[word] += 1
                    if word in blacklist_dict:
                        ads_words[word] += 1

plt.figure()
plt.bar(range(len(ads_words)), list(ads_words.values()), align='center', color='b')
plt.xticks(range(len(ads_words)), list(ads_words.keys()), fontsize=10, rotation=90)
plt.savefig('ads_words_before.png', dpi=600, quality=100)

par_freq_words = freq_words.most_common(opt.top_k/2)
list_value = []
list_key = []
for record in par_freq_words:
    list_key.append(record[0])
    list_value.append(record[1])

non_ads_words = list(set(ads_words)&set(whitelist_dict))

for naw in non_ads_words:
    print(u'===> overlappling words: {k}'.format(k=naw))
    del ads_words[naw]

print('===> Ploting the Ads and Non-Ads words')
plt.figure()
plt.bar(range(len(ads_words)), list(ads_words.values()), align='center', color='b')
plt.xticks(range(len(ads_words)), list(ads_words.keys()), fontsize=10, rotation=90)
plt.savefig('ads_words_after.png', dpi=600, quality=100)

plt.figure()
plt.bar(range(len(par_freq_words)), list_value, align='center', color='r')
plt.xticks(range(len(par_freq_words)), list_key, fontsize=10, rotation=90)
plt.savefig('normal_words.png', dpi=600, quality=100)

print('======== ads words ========')
for key,value in ads_words.iteritems():
    print(u'{k} --> {v}'.format(k=key,v=value))
print('======== ads words ========')

print('===> Filtering the Ads Videos')
sus_files = []
for index, trans_file in enumerate(f_list):
    ads_count = 0
    rel_count = 0

    with codecs.open('/'.join([trans_path, trans_file]), encoding='utf-8') as fr:
        lines = fr.read().splitlines()

    if len(lines) == 0:
        continue

    for line in lines:
        if len(line.split('\t')) == 2:
            if opt.folder == 'english':
                remove_freq_list = lines[0].split()[:-2]
                content = ' '.join(remove_freq_list)

                text = nltk.word_tokenize(content)
                lemmatized_text = []
                for word in text:
                    lemmatized_text.append(lemmatizer.lemmatize(word))

                #print(Diff(text,lemmatized_text))

                tagged = nltk.pos_tag(lemmatized_text)
                entities = nltk.chunk.ne_chunk(tagged)

                '''
                fdist = FreqDist(lemmatized_text)
                tab = fdist.tabulate(10, cumulative=False)
                fdist.plot(10, cumulative=False)
                '''
            elif opt.folder == 'chinese':
                content = line.split('\t')[0]
                lemmatized_text = jieba.cut(content, cut_all=False)
            else:
                print('error: unacceptable folder name')

            for word in lemmatized_text:
                #print(u'{k}'.format(k=word))
                if word in ads_words:
                    ads_count += 1
                elif word in whitelist_dict:
                    rel_count += 1


    print("===> file " + trans_file + " | ads occurrence: " + str(ads_count) + " | relevant words occurrence: " + str(rel_count))
    if ads_count > opt.threshold:# and rel_count < opt.threshold:
        print(''.join(['Suspicious:', trans_file]))
'''
for sus_file in sus_files:
    print(''.join(['Suspicious:', sus_file]))

plt.figure()
diff_words = Diff(freq_words, ads_words)
list_value = []
list_key = []
for k, v in freq_words.items():
    if k in diff_words:
        list_key.append(k)
        list_value.append(v)

plt.bar(range(len(diff_words)), list_value, align='center', color='g')
plt.xticks(range(len(diff_words)), list_key, fontsize=10, rotation=90)
plt.savefig('diff_words.png')
'''

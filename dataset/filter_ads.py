#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import os
import jieba
import argparse
from os import walk
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from collections import Counter
import matplotlib.pylab as plt
import codecs

lemmatizer = WordNetLemmatizer()

parser = argparse.ArgumentParser(description='extract_frame: extract frames and words')
parser.add_argument('--folder', type=str, default="english", help='sub folder in dataset')
parser.add_argument('--dataset', type=str, default="AlphaGo", help='name of the news event')
parser.add_argument('--video_format', type=str, default=".mp4", help='format of input videos')
parser.add_argument('--transcript_format', type=str, default=".txt", help='format of output audios')
parser.add_argument('--top_k', type=int, default=100, help='top words from blacklist of whitelist')
parser.add_argument('--blacklist_threshold', type=int, default=20, help='treshold for filtering out the videos')
parser.add_argument('--whitelist_threshold', type=int, default=30, help='treshold for filtering out the videos')
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

f_list = []
for (dirpath, dirnames, filenames) in walk(trans_path):
    f_list.extend(filenames)

def init_black_white_list():
    '''
    initailize the whitelist and blacklist
    sample path: './AlphaGo/english/blacklist.txt' or './AlphaGo/english/whitelist.txt'

    format in blacklist.txt or whitelist.txt:
        word freq
        of 999
        a 222
        that 111
        ....

    return:
        blacklist_dict, whitelist_dict: k-word, v-freq
    '''

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

    # eliminate the intersected words in blacklist with whitelist
    intersection = list(set(blacklist_dict.keys()) & set(whitelist_dict.keys()))
    for k,v in blacklist_dict.items():
        if k in intersection:
            del blacklist_dict[k]

    return blacklist_dict, whitelist_dict

def count_occurrence(blacklist_dict, whitelist_dict):
    '''
    count the occurrence of blacklist words as TF, and the occurrence of whitelist words as IDF
    the count is global for all transcripts

    return:
        tf_count, idf_count, total_count: k-word, v-count
    '''

    tf_count = Counter()
    idf_count = Counter()
    total_count = Counter()

    print('===> reading transcript files...')
    for index, trans_file in enumerate(f_list):
        #print(''.join(['===> Processing: ', trans_file]))
        with codecs.open('/'.join([trans_path, trans_file]), encoding='utf-8') as fr:
            lines = fr.read().splitlines()

        if len(lines) == 0:
            continue

        for line in lines:
            if not len(line.split('\t')) == 2:
                continue

            if opt.folder == 'english':
                remove_freq_list = lines[0].split()[:-2]
                content = ' '.join(remove_freq_list)

                text = nltk.word_tokenize(content)
                lemmatized_text = []
                for word in text:
                    lemmatized_text.append(lemmatizer.lemmatize(word))

                tagged = nltk.pos_tag(lemmatized_text)
                entities = nltk.chunk.ne_chunk(tagged)

            elif opt.folder == 'chinese':
                content = line.split('\t')[0]
                lemmatized_text = jieba.cut(content, cut_all=False)
            else:
                print('error: unacceptable folder name')

            for word in lemmatized_text:
                total_count[word] += 1
                if word in blacklist_dict:
                    tf_count[word] += 1
                if word in whitelist_dict:
                    idf_count[word] += 1

    return tf_count, idf_count, total_count

def plot_figure(tf_count, idf_count, total_count):
    '''
    plot the count of the tf words occurrence and idf word occurrence
    chinese words is encoded in utf-8 and needs special font for matplotlib
    '''

    if opt.folder=='chinese':
        import matplotlib.font_manager as mfm
        font_path = "matplotlib/SimHei.ttf"
        prop = mfm.FontProperties(fname=font_path, size=5)


    print('===> ploting the blacklist occurrence')
    plt.figure()
    plt.bar(range(len(tf_count)), list(tf_count.values()), align='center', color='b')

    if opt.folder == 'english':
        plt.xticks(range(len(tf_count)), list(tf_count.keys()), fontsize=10, rotation=90)
    elif opt.folder == 'chinese':
        plt.xticks(range(len(tf_count)), list(tf_count.keys()), rotation=90, fontproperties=prop)

    plt.savefig('plot/occurrence_blacklist.png', dpi=600, quality=100)

    print('===> ploting the whitelist occurrence')
    plt.figure()
    plt.bar(range(len(idf_count)), list(idf_count.values()), align='center', color='b')

    if opt.folder == 'english':
        plt.xticks(range(len(idf_count)), list(idf_count.keys()), fontsize=10, rotation=90)
    elif opt.folder == 'chinese':
        plt.xticks(range(len(idf_count)), list(idf_count.keys()), rotation=90, fontproperties=prop)

    plt.savefig('plot/occurrence_whitelist.png', dpi=600, quality=100)

    par_total_count = total_count.most_common(opt.top_k)
    list_value = []
    list_key = []
    for record in par_total_count:
        list_key.append(record[0])
        list_value.append(record[1])

    print('===> ploting the total occurrence')
    plt.figure()
    plt.bar(range(len(par_total_count)), list_value, align='center', color='r')

    if opt.folder == 'english':
        plt.xticks(range(len(par_total_count)), list_key, fontsize=10, rotation=90)
    elif opt.folder == 'chinese':
        plt.xticks(range(len(par_total_count)), list_key, rotation=90, fontproperties=prop)

    plt.savefig('plot/occurrence_total.png', dpi=600, quality=100)

def filter_ads_videos(blacklist_dict, whitelist_dict):
    '''
    count the blacklist words and whitelist words in each transcript, output the occurrence and desision

    need to tweek:
        --blacklist_threshold
        --whitelist_threshold
    '''
    print('===> filtering the ads videos')
    sus_files = []
    for index, trans_file in enumerate(f_list):
        ads_count = 0
        rel_count = 0

        with codecs.open('/'.join([trans_path, trans_file]), encoding='utf-8') as fr:
            lines = fr.read().splitlines()

        if len(lines) == 0:
            continue

        for line in lines:
            if not len(line.split('\t')) == 2:
                continue

            if opt.folder == 'english':
                remove_freq_list = lines[0].split()[:-2]
                content = ' '.join(remove_freq_list)

                text = nltk.word_tokenize(content)
                lemmatized_text = []
                for word in text:
                    lemmatized_text.append(lemmatizer.lemmatize(word))

                tagged = nltk.pos_tag(lemmatized_text)
                entities = nltk.chunk.ne_chunk(tagged)

            elif opt.folder == 'chinese':
                content = line.split('\t')[0]
                lemmatized_text = jieba.cut(content, cut_all=False)
            else:
                print('error: unacceptable folder name')

            for word in lemmatized_text:
                if word in blacklist_dict:
                    ads_count += 1
                if word in whitelist_dict:
                    rel_count += 1

        decsion = '\033[92m'+'normal'+'\033[0m'
        if ads_count > opt.blacklist_threshold:
            decsion = '\033[91m'+'advertising'+'\033[0m'
        elif rel_count < opt.whitelist_threshold:
            decsion = '\033[93m'+'unrelevant'+'\033[0m'

        print('===> {s}: ads word count:{a} relevance count:{r} | {d}'.format(s=trans_file, a=ads_count, r=rel_count, d=decsion))


def main():
    blacklist_dict, whitelist_dict = init_black_white_list()
    tf_count, idf_count, total_count = count_occurrence(blacklist_dict, whitelist_dict)
    plot_figure(tf_count, idf_count, total_count)
    filter_ads_videos(blacklist_dict, whitelist_dict)

if __name__ == '__main__':
    main()
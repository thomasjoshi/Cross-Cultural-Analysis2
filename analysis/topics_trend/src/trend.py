#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import pickle
import pandas as pd
import argparse
import re
from collections import defaultdict


def extract_topics(filename):
    topic_to_cats = defaultdict(set)
    category = None
    topics = set()
    with open(filename) as f:
        for line in f:
            line = line[:-1]
            if not line:
                continue
            search = re.search(r'^[0-9]+\) (.+)', line)
            if search:
                topic = search.group(1)
                topics.add(topic)
                topic_to_cats[topic].add(category)
            else:
                category = line
    return topics, topic_to_cats


def update_trends(trend_data, topics, timeframe, geo):
    # df_7d = pd.DataFrame()
    trend = TrendReq(tz=240, geo=geo)
    for topic in topics:
        print(f'Working on topic "{topic}"')
        trend.build_payload([topic], timeframe=timeframe, geo=geo)
        tp = trend.interest_over_time()
        # trend.build_payload([keyword], timeframe='now 7-d', geo=geo)
        # tp_7d = trend.interest_over_time()
        if tp.empty:
            continue
        trend_data = pd.concat((trend_data, tp.iloc[:, 0]), axis=1)
        # df_7d = pd.concat((df_7d, tp_7d.iloc[:, 0]), axis=1)
    return trend_data


def calc_stats(s, rolling, bias=10, threshold=3):
    idx = s.idxmax()
    rolling = s.rolling(rolling).mean()
    scores = (s + bias) / (rolling + bias)
    result = pd.Series([scores[idx], (scores > threshold).sum(), s.idxmax()], index=['score', 'spikes', 'time'])
    result.name = s.name
    return result


def plot_topic(topic, trend_data, rolling):
    trend_data[topic].plot(label=topic)
    if rolling > 0:
        rolling_data = trend_data.rolling(rolling).mean()
        rolling_data[topic].plot(label=f'{topic}_rolling_{rolling}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='analyze topic trends using Google Trends')
    parser.add_argument('-i', '--input', help='input topics')
    parser.add_argument('-a', '--additional', nargs='*', help='additional topics')
    parser.add_argument('-o', '--output', help='output data')
    parser.add_argument('-d', '--data', help='existing data file to read')
    parser.add_argument('-p', '--plot', nargs='*', help='topics to plot')
    parser.add_argument('-f', '--filters', nargs='*', help='filter categories')
    parser.add_argument('-g', '--geo', default='US', help='geo location')
    parser.add_argument('-t', '--timeframe', default='2014-01-01 2018-12-31', help='timeframe to search')
    parser.add_argument('-r', '--rolling', type=int, default=24, help='rolling window size')
    args = parser.parse_args()

    topics_filename = args.input
    add_topics = args.additional
    output_filename = args.output
    existing_data_filename = args.data
    plot_topics = args.plot
    filter_categories = args.filters
    timeframe = args.timeframe
    geo = args.geo
    rolling = args.rolling

    if topics_filename:
        topics, topic_to_cats = extract_topics(topics_filename)
    else:
        topics = set()
        topics_to_cats = None
    if add_topics:
        topics.update(set(add_topics))
    if filter_categories and topics_filename:
        topics = {topic for topic in topics if not topic_to_cats[topic].isdisjoint(set(filter_categories))}
    if existing_data_filename:
        with open(existing_data_filename, 'rb') as f:
            trend_data = pickle.load(f)
        topics.difference_update(set(trend_data.columns))
    else:
        trend_data = pd.DataFrame()
    trend_data = update_trends(trend_data, topics, timeframe, geo)
    if output_filename:
        with open(output_filename, 'wb') as f:
            pickle.dump(trend_data, f)

    result = pd.concat([calc_stats(trend_data[s], rolling) for s in trend_data.columns], axis=1).T
    result = pd.DataFrame.sort_values(result, 'score', ascending=False)
    print(result)

    if plot_topics:
        for topic in plot_topics:
            plot_topic(topic, trend_data, rolling)
        plt.legend()
        plt.show()

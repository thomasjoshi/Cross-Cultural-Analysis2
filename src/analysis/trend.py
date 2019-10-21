#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import json
import matplotlib.pyplot as plt
import pandas as pd
import re
from collections import defaultdict
from pytrends.request import TrendReq


def extract_topics(filename):
    cat_to_topics = defaultdict(list)
    category = None
    with open(filename) as f:
        for line in f:
            line = line[:-1]
            if not line:
                continue
            search = re.search(r'^[0-9]+\) (.+)', line)
            if search:
                topic = search.group(1)
                cat_to_topics[category].append(topic)
            else:
                category = line
    return cat_to_topics


def update_trends(trend_data, topics, timeframe, geo):
    trend = TrendReq(tz=240, geo=geo)
    for topic in topics:
        print(f'Working on topic "{topic}"')
        trend.build_payload([topic], timeframe=timeframe, geo=geo)
        tp = trend.interest_over_time()
        if tp.empty:
            continue
        trend_data = pd.concat((trend_data, tp.iloc[:, 0]), axis=1)
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


def trend(topics_path=None, add_topics_path=None, output_path=None, append=False, plot_topics=None,
          filter_categories=None, timeframe='2014-01-01 2018-12-31', geo='US', rolling=24):
    topics_type = 'json'
    if not topics_path:
        cat_to_topics = {}
    elif topics_path.endswith('.' + topics_type):
        with open(topics_path) as f:
            cat_to_topics = defaultdict(list, json.load(f))
    else:
        cat_to_topics = extract_topics(topics_path)
        dot_pos = topics_path.rfind('.')
        topics_new_path = (topics_path[:dot_pos] if dot_pos != -1 else topics_path) + '.' + topics_type
        with open(topics_new_path, 'w') as f:
            json.dump(cat_to_topics, f)
    topics = set.union(*(set(v) for v in cat_to_topics.values()))

    if add_topics_path:
        with open(add_topics_path) as f:
            topics.update(f.read().splitlines())
    if filter_categories and topics_path:
        filter_topics = set.union(*(set(cat_to_topics[c]) for c in filter_categories))
        topics.intersection_update(filter_topics)
    if output_path and append:
        trend_data = pd.read_pickle(output_path)
        topics.difference_update(set(trend_data.columns))
    else:
        trend_data = pd.DataFrame()

    trend_data = update_trends(trend_data, topics, timeframe, geo)
    if output_path:
        trend_data.to_pickle(output_path)

    result = pd.concat([calc_stats(trend_data[s], rolling) for s in trend_data.columns], axis=1).T
    result = pd.DataFrame.sort_values(result, 'score', ascending=False)
    print(result)

    if plot_topics:
        for topic in plot_topics:
            plot_topic(topic, trend_data, rolling)
        plt.legend()
        plt.show()


def main():
    parser = argparse.ArgumentParser(description='analyze topic trends using Google Trends')
    parser.add_argument('-i', '--input', help='path to topics with categories, json or text')
    parser.add_argument('-d', '--additional', help='path to additional topics text file')
    parser.add_argument('-o', '--output', help='output data')
    parser.add_argument('-a', '--append', action='store_true', help='whether to append to existing data')
    parser.add_argument('-p', '--plot', nargs='*', help='topics to plot')
    parser.add_argument('-f', '--filters', nargs='*', help='filter categories')
    parser.add_argument('-t', '--timeframe', default='2014-01-01 2018-12-31', help='timeframe to search')
    parser.add_argument('-g', '--geo', default='US', help='geo location')
    parser.add_argument('-r', '--rolling', type=int, default=24, help='rolling window size')
    args = parser.parse_args()
    trend(args.input, args.additional, args.output, args.append, args.plot, args.filters, args.timeframe, args.geo,
          args.rolling)


if __name__ == '__main__':
    main()

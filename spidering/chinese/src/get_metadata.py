#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from spider import Spider
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='get metadata for Chinese videos')
    parser.add_argument('query', help='the query for videos')
    parser.add_argument('-n', '--quantity', type=int, default=200, help='number of videos to collect')
    parser.add_argument('-o', '--output', default='output', help='output directory')
    parser.add_argument('-u', '--update', action='store_true', help='whether to start over or to update existing data')
    args = parser.parse_args()

    query = args.query
    quantity = args.quantity
    output = args.output
    update = args.update

    if not os.path.exists(output):
        os.makedirs(output)

    query_filename = os.path.join(output, 'query.txt')
    url_filename = os.path.join(output, 'urls.txt')
    data_filename = os.path.join(output, 'data')
    title_filename = os.path.join(output, 'titles.txt')
    desc_filename = os.path.join(output, 'descriptions.txt')

    metadata_parser = Spider()
    if update:
        metadata_parser.load_data(data_filename)
    metadata_parser.set_query(query)
    metadata_parser.get_urls(Spider.BILIBILI, quantity)
    metadata_parser.save_urls(url_filename)
    metadata_parser.get_urls(Spider.TENCENT, quantity)
    metadata_parser.save_urls(url_filename)
    metadata_parser.get_urls(Spider.IQIYI, quantity)
    metadata_parser.save_urls(url_filename)
    metadata_parser.get_urls(Spider.YOUKU, quantity)
    metadata_parser.save_urls(url_filename)
    metadata_parser.get_data()
    metadata_parser.save_urls(url_filename)
    metadata_parser.save_data(data_filename)

    metadata_parser.export_query(query_filename)
    metadata_parser.export_titles(title_filename)
    metadata_parser.export_descriptions(desc_filename)

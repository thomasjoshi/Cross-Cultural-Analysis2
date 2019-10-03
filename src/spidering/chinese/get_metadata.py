#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import os
from spider import Spider


def get_metadata(query, quantity=200, output='output', append=False):
    if not os.path.isdir(output):
        os.makedirs(output)

    query_filename = os.path.join(output, 'query.txt')
    url_filename = os.path.join(output, 'urls.json')
    metadata_filename = os.path.join(output, 'metadata')
    title_filename = os.path.join(output, 'titles.json')
    title_content_filename = os.path.join(output, 'titles.txt')
    desc_filename = os.path.join(output, 'descriptions.json')
    desc_content_filename = os.path.join(output, 'descriptions.txt')

    spider = Spider()
    if append:
        spider.load_metadata(metadata_filename)
    spider.set_query(query)
    spider.get_urls(Spider.BILIBILI, quantity)
    spider.save_urls(url_filename)
    spider.get_urls(Spider.TENCENT, quantity)
    spider.save_urls(url_filename)
    spider.get_urls(Spider.IQIYI, quantity)
    spider.save_urls(url_filename)
    spider.get_urls(Spider.YOUKU, quantity)
    spider.save_urls(url_filename)
    spider.get_data()
    spider.save_urls(url_filename)
    spider.save_metadata(metadata_filename)

    spider.export_query(query_filename)
    spider.export_titles(title_filename)
    spider.export_titles(title_content_filename, content_only=True)
    spider.export_descriptions(desc_filename)
    spider.export_descriptions(desc_content_filename, content_only=True)


def main():
    parser = argparse.ArgumentParser(description='get metadata for Chinese videos')
    parser.add_argument('query', help='the query for videos')
    parser.add_argument('-n', '--quantity', type=int, default=200, help='number of videos to collect from each source')
    parser.add_argument('-o', '--output', default='output', help='output directory')
    parser.add_argument('-a', '--append', action='store_true', help='whether to append to existing data')
    args = parser.parse_args()
    get_metadata(args.query, args.quantity, args.output, args.append)


if __name__ == '__main__':
    main()

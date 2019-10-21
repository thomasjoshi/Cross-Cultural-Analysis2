#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import os
from spider import Spider


def get_metadata(query, quantity=200, output='output', append=False, key=None, sources=None):
    if not os.path.isdir(output):
        os.makedirs(output)
    if key and os.path.isfile(key):
        with open(key) as f:
            key = f.read().replace('\n', '')
    if not sources:
        sources = Spider.ALL_SOURCES
    else:
        sources = set(s.lower() for s in sources).intersection(set(Spider.ALL_SOURCES))

    query_filename = os.path.join(output, 'query.txt')
    metadata_filename = os.path.join(output, 'metadata')
    title_filename = os.path.join(output, 'titles.json')
    title_content_filename = os.path.join(output, 'titles.txt')
    desc_filename = os.path.join(output, 'descriptions.json')
    desc_content_filename = os.path.join(output, 'descriptions.txt')

    spider = Spider(query)
    if append and os.path.isfile(metadata_filename):
        spider.load(metadata_filename)
    for source in sources:
        spider.get_metadata(source, quantity, key=key)
        spider.save(metadata_filename)

    spider.export_query(query_filename)
    spider.export_titles(title_filename)
    spider.export_titles(title_content_filename, content_only=True)
    spider.export_descriptions(desc_filename)
    spider.export_descriptions(desc_content_filename, content_only=True)
    return spider


def main():
    parser = argparse.ArgumentParser(description='get metadata for Chinese videos')
    parser.add_argument('query', help='the query for videos')
    parser.add_argument('-n', '--quantity', type=int, default=200, help='number of videos to collect from each source')
    parser.add_argument('-o', '--output', default='output', help='output directory')
    parser.add_argument('-a', '--append', action='store_true', help='whether to append to existing data')
    parser.add_argument('-k', '--key', help='key for Youtube API, string or path to text file')
    parser.add_argument('-s', '--sources', nargs='*', help='filter sources')
    args = parser.parse_args()
    get_metadata(args.query, args.quantity, args.output, args.append, args.key, args.sources)


if __name__ == '__main__':
    main()

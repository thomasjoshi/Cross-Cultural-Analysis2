import common
import sys
from iqiyi import get_responses

num = 200
sources = ('', 'iqiyi', 'qq', 'sohu', 'youku', 'tudou', 'acfun', 'bilibili', 'ifeng', 'cntv', 'm1905')

# keyword = 'alphago'
# output_dir = 'AlphaGo'
# source = 2
keyword = sys.argv[1]
output_dir = sys.argv[2]
source = int(sys.argv[3])

url_filename = 'urls_' + sources[source] + '.txt'
desc_filename = 'desc_' + sources[source] + '.txt'
title_filename = 'titles_' + sources[source] + '.txt'
data_filename = 'data_' + sources[source]

ps = get_responses(keyword, num, duration=1, source=source)
urls = [p[0] for p in ps]
common.save_urls(urls, url_filename, 'a')
videos = common.get_videos_info(ps)
common.save_data(videos, data_filename)
common.save_des(videos, desc_filename, 'a')
common.save_titles(videos, title_filename, 'a')

common.download(url_filename, output_dir)

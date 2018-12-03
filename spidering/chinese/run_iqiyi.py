import common
from iqiyi import get_responses

num = 1
sources = ('', 'iqiyi', 'qq', 'sohu', 'youku', 'tudou', 'acfun', 'bilibili', 'ifeng', 'cntv', 'm1905')
url_filename = 'urls.txt'
desc_filename = 'desc.txt'
title_filename = 'titles.txt'

# keyword = 'alphago'
# output_dir = 'AlphaGo'
keyword = sys.argv[1]
output_dir = sys.argv[2]
for source in (1, 2, 7):
    print('Video source: %s' % sources[source])
    data_filename = 'data_iqiyi_' + sources[source]

    ps = get_responses(keyword, num, duration=1, source=source)
    urls = [p[0] for p in ps]
    common.save_urls(urls, url_filename, 'w')
    videos = common.get_videos_info(ps)
    common.save_data(videos, data_filename)
    common.save_des(videos, desc_filename, 'w')
    common.save_titles(videos, title_filename, 'a')
common.download(url_filename, output_dir)

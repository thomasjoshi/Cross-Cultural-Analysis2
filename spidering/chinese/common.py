import pickle
import sys
from subprocess import call
import tencent
import iqiyi
# import bilibili


def save_data(videos, filename):
    with open(filename, 'wb') as f:
        pickle.dump(videos, f)


def load_data(filename):
    with open(filename, 'rb') as f:
        videos = pickle.load(f)
    return videos


def save_urls(urls, filename):
    with open(filename, 'w') as f:
        f.writelines(url + '\n' for url in urls)


def save_des(videos, filename):
    with open(filename, 'w') as f:
        f.writelines(v['description'] + '\n' for v in videos if v['description'] is not None)


def download(filename, output_dir='AlphaGo'):
    with open(filename, 'r') as f:
        for url in f:
            call(['you-get', '-o', output_dir, url])


def get_videos_info(ps):
    result = []
    for i, p in enumerate(ps):
        print('Parsing video %d / %d' % (i + 1, len(ps)))
        url = p[0]
        try:
            if 'qq.com' in url:
                result.append(tencent.parse(p))
            elif 'iqiyi.com' in url:
                result.append(iqiyi.parse(p))
            # elif 'bilibili.com' in url:
            #     result.append(bilibili.parse(p))
            else:
                print('Unknown site: ' + url)
        except:
            print('Error: ' + url)
    return result


if __name__ == '__main__':
    search_source = 'iqiyi'
    keyword = 'alphago'
    output_dir = 'AlphaGo'

    # search_source = sys.argv[1]
    # keyword = sys.argv[2]
    # output_dir = sys.argv[3]
    num = 500
    init = True

    data_filename = 'data_' + search_source
    url_filename = 'urls_' + search_source + '.txt'
    desc_filename = 'desc_' + search_source + '.txt'
    get_response_funs = {'tencent': tencent.get_responses, 'iqiyi': iqiyi.get_responses}
    # 'bilibili': bilibili.get_responses
    if init:
        ps = get_response_funs[search_source](keyword, num)
        urls = [p[0] for p in ps]
        save_urls(urls, url_filename)
        videos = get_videos_info(ps)
        save_data(videos, data_filename)
        save_des(videos, desc_filename)
    else:
        videos = load_data(data_filename)

    # download(url_filename, output_dir)

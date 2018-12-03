import pickle
from subprocess import call
import tencent
import iqiyi
import bilibili


def save_data(videos, filename):
    with open(filename, 'wb') as f:
        pickle.dump(videos, f)


def load_data(filename):
    with open(filename, 'rb') as f:
        videos = pickle.load(f)
    return videos


def save_urls(urls, filename, flag='a'):
    with open(filename, flag) as f:
        f.writelines(url + '\n' for url in urls)


def save_des(videos, filename, flag='a'):
    with open(filename, flag) as f:
        f.writelines(v['description'] + '\n' for v in videos if v['description'] is not None)


def save_titles(videos, filename, flag='a'):
    with open(filename, flag) as f:
        f.writelines(v['title'] + '\n' for v in videos if v['title'] is not None)


def download(filename, output_dir):
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
            elif 'bilibili.com' in url:
                result.append(bilibili.parse(p))
            else:
                print('Unknown site: ' + url)
        except Exception as e:
            print('Error: ' + url)
            print(e)
    return result

import pickle
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re


class Parser:
    UNKNOWN = 0
    BILIBILI = 1
    TENCENT = 2
    IQIYI = 3
    YOUKU = 4

    @staticmethod
    def get_source_and_vid(url):
        if 'bilibili.com' in url:
            return Parser.BILIBILI, re.search(r'(av[0-9]*)', url).group(1)
        elif 'qq.com' in url:
            return Parser.TENCENT, re.search(r'/([^/]*?)\.html', url).group(1)
        elif 'iqiyi.com' in url:
            return Parser.IQIYI, re.search(r'/([^/]*?)\.html', url).group(1)
        elif 'youku.com' in url:
            return Parser.YOUKU, re.search(r'/([^/]*?)\.html', url).group(1)
        else:
            return Parser.UNKNOWN, None

    def __init__(self):
        self.header = {'User-Agent': 'Chrome/72.0.3626.109'}
        self.urls = set()  # urls of videos
        self.data = {}  # video metadata, vid -> metadata

    def save_data(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self.urls, self.data), f)

    def load_data(self, filename):
        with open(filename, 'rb') as f:
            urls, data = pickle.load(f)
            self.urls.update(urls)
            self.data.update(data)

    def save_urls(self, filename):
        with open(filename, 'w') as f:
            f.writelines(url + '\n' for url in self.urls)

    def load_urls(self, filename):
        with open(filename) as f:
            self.urls.update(f.read().splitlines())

    def export_descriptions(self, filename):
        with open(filename, 'w') as f:
            f.writelines(
                k + '\t' + v['description'] + '\n' for k, v in self.data.items() if v['description'] is not None)

    def export_titles(self, filename):
        with open(filename, 'w') as f:
            f.writelines(k + '\t' + v['title'] + '\n' for k, v in self.data.items() if v['title'] is not None)

    def download(self, output_dir, filters=('bilibili.com', 'qq.com', 'iqiyi.com', 'youku.com')):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        urls = [url for url in self.urls if any(s in url for s in filters)]
        for i, url in enumerate(urls):
            vid = self.get_source_and_vid(url)[1]
            print(f'Downloading video {i + 1} / {len(urls)}')
            os.system('yes N | you-get -o ' + output_dir + ' -O ' + vid + ' ' + url)

    def get_urls(self, source, query, num, duration=1, order=0, tids_1=0, tids_2=0, scr=1):
        bilibili_orders = ['totalrank', 'click', 'pubdate', 'dm', 'stow']
        iqiyi_sources = ['', 'iqiyi', 'qq', 'sohu', 'youku', 'tudou', 'acfun', 'bilibili', 'ifeng', 'cntv', 'm1905']
        if source == Parser.BILIBILI:
            fs = 'https://search.bilibili.com/all?keyword=' + query + '&order=' + bilibili_orders[
                order] + '&duration=' + str(duration) + '&tids_1=' + str(tids_1) + '&tids_2=' + str(tids_2) + '&page=%d'
        elif source == Parser.TENCENT:
            fs = 'https://v.qq.com/x/search/?q=' + query + '&cxt=%%3Dduration%%3D' + str(duration) + '&cur=%d'
        elif source == Parser.IQIYI:
            fs = 'https://so.iqiyi.com/so/q_' + query + '_ctg__t_' + str(
                duration + 1 if duration != 0 else 0) + '_page_%d' + '_p_1_qc_0_rd__site_' + iqiyi_sources[
                     scr] + '_m_1_bitrate_'
        elif source == Parser.YOUKU:
            fs = 'https://so.youku.com/search_video/q_' + query + '?aaid=0&lengthtype=' + str(duration) + '&pg=%d'
        else:
            print('Unknown source')
            return
        page = 1
        count = 0
        while count < num:
            prev_count = count
            print(f'Page {page}')
            s = fs % page
            response = requests.get(s, headers=self.header)
            if response.status_code != 200:
                print('Search failed: ' + s)
                return
            if source == Parser.BILIBILI:
                soup = BeautifulSoup(response.text, 'html.parser')
                video_items = soup.find_all('li', {'class': 'video matrix'})
            elif source == Parser.TENCENT:
                soup = BeautifulSoup(response.text, 'html.parser')
                video_items = soup.find_all('div', {'class': 'result_item result_item_h _quickopen'})
            elif source == Parser.IQIYI:
                soup = BeautifulSoup(response.text, 'html.parser')
                video_items = soup.find_all('li', {'class': 'list_item'})
            elif source == Parser.YOUKU:
                video_items = list(set(re.findall(r'(id_.*?)\.html', response.text)))
            else:
                print('Unknown source')
                return
            for v in video_items:
                if source == Parser.BILIBILI:
                    url = 'https://www.bilibili.com/video/' + v.find('span', {'class': 'type avid'}).text
                elif source == Parser.TENCENT:
                    url = v.a['href']
                elif source == Parser.IQIYI:
                    url = v.find({'a', 'href'})['href']
                elif source == Parser.YOUKU:
                    url = 'https://v.youku.com/v_show/' + v + '.html'
                else:
                    print('Unknown source')
                    return
                resp = requests.head(url, headers=self.header)
                if resp.status_code // 100 >= 4 or url in self.urls:
                    continue
                self.urls.add(url)
                count += 1
                print(f'Got video URL {count} / {num}')
                if count == num:
                    break
            if count == prev_count:
                break
            page += 1

    def get_data_from_url(self, url):
        # parses metadata from a single url, updates self.data
        source, vid = self.get_source_and_vid(url)
        if vid in self.data:
            return
        response = requests.get(url, headers=self.header)
        if response.status_code != 200:
            print('Video page failed: ' + url)
            return
        if source == Parser.BILIBILI:
            s = re.search(r'window.__INITIAL_STATE__=({.*?});', response.text).group(1)
            d = json.loads(s)['videoData']
            self.data[vid] = {'vid': vid, 'url': url, 'title': d['title'], 'description': d['desc'],
                              'duration': d['duration'], 'publish_time': datetime.fromtimestamp(d['pubdate']),
                              'last_time': datetime.fromtimestamp(d['ctime']), 'poster': d['owner']['name']}
        elif source == Parser.TENCENT:
            s = re.search(r'var\s*VIDEO_INFO\s*=\s*({.*?})[;\n]', response.text, re.DOTALL).group(1)
            d = json.loads(s)
            pt = d['publish_date']
            if pt is not None and pt != '' and pt[0] != '0':
                if len(pt) > 10:
                    publish_time = datetime.strptime(pt, '%Y-%m-%d %H:%M:%S')
                else:
                    publish_time = datetime.strptime(pt, '%Y-%m-%d')
            else:
                publish_time = None
            lt = d['modify_time']
            if lt is not None and lt != '' and lt[0] != '0':
                if len(lt) > 10:
                    last_time = datetime.strptime(lt, '%Y-%m-%d %H:%M:%S')
                else:
                    last_time = datetime.strptime(lt, '%Y-%m-%d')
            else:
                last_time = None
            self.data[vid] = {'vid': vid, 'url': url, 'title': d['title'], 'description': d['desc'],
                              'duration': int(d['duration']), 'publish_time': publish_time, 'last_time': last_time,
                              'poster': d['upload_qq']}
        elif source == Parser.IQIYI:
            s = re.search(r'video-info=\'({.*?})\'', response.text).group(1)
            d = json.loads(s)
            poster = d['user']['name'] if 'user' in d else None
            self.data[vid] = {'vid': vid, 'url': url, 'title': d['name'], 'description': d['description'],
                              'duration': d['duration'],
                              'publish_time': datetime.fromtimestamp(d['firstPublishTime'] * 1e-3),
                              'last_time': datetime.fromtimestamp(d['lastPublishTime'] * 1e-3), 'poster': poster,
                              'subtitle': d['subtitle']}
        elif source == Parser.YOUKU:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('meta', {'name': 'title'})['content']
            description = soup.find('meta', {'name': 'description'})['content']
            duration = round(float(re.search(r'seconds:\s*\'(.*?)\'', response.text).group(1)))
            pt = soup.find('meta', {'itemprop': 'datePublished'})['content']
            publish_time = datetime.strptime(pt, '%Y-%m-%d %H:%M:%S') if pt != '' else None
            lt = soup.find('meta', {'itemprop': 'uploadDate'})['content']
            last_time = datetime.strptime(lt, '%Y-%m-%d %H:%M:%S') if lt != '' else None
            poster = re.search(r'videoOwner:\s*\'(.*?)\'', response.text).group(1)
            self.data[vid] = {'vid': vid, 'url': url, 'title': title, 'description': description, 'duration': duration,
                              'publish_time': publish_time, 'last_time': last_time, 'poster': poster}
        else:
            print('Unknown source')
            return

    def get_data(self):
        # processes all urls in self.urls, updates self.data
        to_remove = set()
        for i, url in enumerate(self.urls):
            print(f'Retrieving metadata {i + 1} / {len(self.urls)}')
            try:
                self.get_data_from_url(url)
            except Exception as e:
                print('Error: ' + url)
                print(e)
                to_remove.add(url)
        self.urls.difference_update(to_remove)

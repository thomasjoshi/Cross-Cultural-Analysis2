import pickle
import os
from subprocess import call
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re


class Parser:
    def __init__(self):
        super().__init__()
        self.header = {'User-Agent': 'Chrome/72.0.3626.109'}
        self.urls = set()  # urls of videos
        self.data = {}  # video metadata, vid -> metadata

    def save_data(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self.urls, self.data), f)

    def load_data(self, filename):
        with open(filename, 'rb') as f:
            self.urls, self.data = pickle.load(f)

    def save_urls(self, filename, flag='w'):
        with open(filename, flag) as f:
            f.writelines(url + '\n' for url in self.urls)

    def load_urls(self, filename):
        with open(filename, 'r') as f:
            for url in f:
                self.urls.add(url.replace('\n', ''))

    def export_descriptions(self, filename):
        with open(filename, 'w') as f:
            f.writelines(v['description'] + '\n' for v in self.data.values() if v['description'] is not None)

    def export_titles(self, filename):
        with open(filename, 'w') as f:
            f.writelines(v['title'] + '\n' for v in self.data.values() if v['title'] is not None)

    def download(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for i, url in enumerate(self.urls):
            print(f'Downloading video {i + 1} / {len(self.urls)}')
            call(['you-get', '-o', output_dir, url])

    def get_data_from_url(self, url):
        # parses metadata from a single url, updates self.data
        if 'bilibili.com' in url:
            self.get_data_from_url_bilibili(url)
        elif 'qq.com' in url:
            self.get_data_from_url_tencent(url)
        elif 'iqiyi.com' in url:
            self.get_data_from_url_iqiyi(url)
        elif 'youku.com' in url:
            self.get_data_from_url_youku(url)
        else:
            print('Unknown site: ' + url)

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

    # Bilibili
    def get_urls_bilibili(self, query, num, order=0, duration=1, tids_1=0, tids_2=0):
        orders = ['totalrank', 'click', 'pubdate', 'dm', 'stow']
        page = 1
        count = 0
        while count < num:
            s = 'https://search.bilibili.com/all?keyword=' + query + '&order=' + orders[order] + '&duration=' + str(
                duration) + '&tids_1=' + str(tids_1) + '&tids_2=' + str(tids_2) + '&page=' + str(page)
            response = requests.get(s, headers=self.header)
            if response.status_code != 200:
                print('Search failed: ' + url)
                return
            soup = BeautifulSoup(response.text, 'html.parser')
            video_items = soup.find_all('li', {'class': 'video matrix'})
            for v in video_items:
                url = 'https://www.bilibili.com/video/' + v.find('span', {'class': 'type avid'}).text
                resp = requests.head(url, headers=self.header)
                if resp.status_code != 200 or url in self.urls:
                    continue
                self.urls.add(url)
                count += 1
                print(f'Got video URL {count} / {num}')
                if count == num:
                    break
            page += 1

    def get_data_from_url_bilibili(self, url):
        response = requests.get(url, headers=self.header)
        if response.status_code != 200:
            print('Video page failed: ' + url)
            return
        s = re.search(r'window.__INITIAL_STATE__=({.*?});', response.text).group(1)
        d = json.loads(s)['videoData']
        vid = d['aid']
        self.data[vid] = {'id': vid, 'url': url, 'title': d['title'], 'description': d['desc'],
                          'duration': d['duration'], 'publish_time': datetime.fromtimestamp(d['pubdate']),
                          'last_time': datetime.fromtimestamp(d['ctime']), 'poster': d['owner']['name']}

    # Tencent
    def get_urls_tencent(self, query, num, duration=1):
        page = 1
        count = 0
        while count < num:
            s = 'https://v.qq.com/x/search/?q=' + query + '&cxt=%3Dduration%3D' + str(duration) + '&cur=' + str(page)
            response = requests.get(s, headers=self.header)
            if response.status_code != 200:
                print('Search failed: ' + url)
                return
            soup = BeautifulSoup(response.text, 'html.parser')
            video_items = soup.find_all('div', {'class': 'result_item result_item_h _quickopen'})
            for v in video_items:
                url = v.a['href']
                if 'qq.com' not in url:
                    continue
                resp = requests.head(url, headers=self.header)
                if resp.status_code != 200 or url in self.urls:
                    continue
                self.urls.add(url)
                count += 1
                print(f'Got video URL {count} / {num}')
                if count == num:
                    break
            page += 1

    def get_data_from_url_tencent(self, url):
        response = requests.get(url, headers=self.header)
        if response.status_code != 200:
            print('Video page failed: ' + url)
            return
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
        vid = d['vid']
        self.data[vid] = {'id': vid, 'url': url, 'title': d['title'], 'description': d['desc'],
                          'duration': int(d['duration']), 'publish_time': publish_time, 'last_time': last_time,
                          'poster': d['upload_qq']}

    # Iqiyi
    def get_urls_iqiyi(self, query, num, source=1, duration=2):
        sources = ['', 'iqiyi', 'qq', 'sohu', 'youku', 'tudou', 'acfun', 'bilibili', 'ifeng', 'cntv', 'm1905']
        page = 1
        count = 0
        while count < num:
            s = 'https://so.iqiyi.com/so/q_' + query + '_ctg__t_' + str(duration) + '_page_' + str(
                page) + '_p_1_qc_0_rd__site_' + sources[source] + '_m_1_bitrate_'
            response = requests.get(s, headers=self.header)
            if response.status_code != 200:
                print('Search failed: ' + url)
                return
            soup = BeautifulSoup(response.text, 'html.parser')
            video_items = soup.find_all('li', {'class': 'list_item'})
            for v in video_items:
                url = v.find({'a', 'href'})['href']
                resp = requests.head(url, headers=self.header)
                if resp.status_code != 200 or url in self.urls:
                    continue
                self.urls.add(url)
                count += 1
                print(f'Got video URL {count} / {num}')
                if count == num:
                    break
            page += 1

    def get_data_from_url_iqiyi(self, url):
        response = requests.get(url, headers=self.header)
        if response.status_code != 200:
            print('Video page failed: ' + url)
            return
        s = re.search(r'video-info=\'({.*?})\'', response.text).group(1)
        d = json.loads(s)
        poster = d['user']['name'] if 'user' in d else None
        vid = re.search(r'iqiyi\.com/(.*?)\.html', url).group(1)
        self.data[vid] = {'id': vid, 'url': url, 'title': d['name'], 'description': d['description'],
                          'duration': d['duration'],
                          'publish_time': datetime.fromtimestamp(d['firstPublishTime'] * 1e-3),
                          'last_time': datetime.fromtimestamp(d['lastPublishTime'] * 1e-3), 'poster': poster,
                          'subtitle': d['subtitle']}

    # Youku
    def get_urls_youku(self, query, num, duration=1):
        page = 1
        count = 0
        while count < num:
            s = 'https://so.youku.com/search_video/q_' + query + '?aaid=0&lengthtype=' + str(duration) + '&pg=' + str(page)
            response = requests.get(s, headers=self.header)
            if response.status_code != 200:
                print('Search failed: ' + url)
                return
            vids = list(set(re.findall(r'id_(.*?)\.html', response.text)))
            for vid in vids:
                url = 'https://v.youku.com/v_show/id_' + vid + '.html'
                resp = requests.head(url, headers=self.header)
                if resp.status_code != 200 or url in self.urls:
                    continue
                self.urls.add(url)
                count += 1
                print(f'Got video URL {count} / {num}')
                if count == num:
                    break
            page += 1

    def get_data_from_url_youku(self, url):
        response = requests.get(url, headers=self.header)
        if response.status_code != 200:
            print('Video page failed: ' + url)
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('meta', {'name': 'title'})['content']
        description = soup.find('meta', {'name': 'description'})['content']
        duration = round(float(re.search(r'seconds:\s*\'(.*?)\'', response.text).group(1)))
        pt = soup.find('meta', {'itemprop': 'datePublished'})['content']
        publish_time = datetime.strptime(pt, '%Y-%m-%d %H:%M:%S') if pt != '' else None
        lt = soup.find('meta', {'itemprop': 'uploadDate'})['content']
        last_time = datetime.strptime(lt, '%Y-%m-%d %H:%M:%S') if lt != '' else None
        poster = re.search(r'videoOwner:\s*\'(.*?)\'', response.text).group(1)
        vid = re.search(r'currentEncodeVid:\s*\'(.*?)\'', response.text).group(1)
        self.data[vid] = {'id': vid, 'url': url, 'title': title, 'description': description, 'duration': duration,
                          'publish_time': publish_time, 'last_time': last_time, 'poster': poster}

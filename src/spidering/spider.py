#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import json
import os
import pickle
import re
import requests
import subprocess
from bs4 import BeautifulSoup
from datetime import datetime

# TODO: Rewrite Spider class to specifically get videos from particular videos
class Spider:
    HEADER = {'User-Agent': 'Chrome/77.0.3865.90'}
    BILIBILI = 'bilibili'
    TENCENT = 'qq'
    IQIYI = 'iqiyi'
    YOUKU = 'youku'
    YOUTUBE = 'youtube'
    ALL_SOURCES = [BILIBILI, TENCENT, IQIYI, YOUKU, YOUTUBE]

    def __init__(self, query=None):
        self.query = query
        # id -> video metadata
        self.metadata = {}

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self.query, self.metadata), f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            self.query, self.metadata = pickle.load(f)

    def export_query(self, filename):
        with open(filename, 'w') as f:
            f.write(self.query)

    def export_descriptions(self, filename, content_only=False):
        with open(filename, 'w') as f:
            if content_only:
                f.writelines(v['description'] + '\n' for v in self.metadata.values() if v['description'])
            else:
                json.dump({k: v['description'] for k, v in self.metadata.items()}, f)

    def export_titles(self, filename, content_only=False):
        with open(filename, 'w') as f:
            if content_only:
                f.writelines(v['title'] + '\n' for v in self.metadata.values() if v['title'])
            else:
                json.dump({k: v['title'] for k, v in self.metadata.items()}, f)

    # def download(self, output_dir, filters=None):
    #     if not os.path.isdir(output_dir):
    #         os.makedirs(output_dir)
    #     urls = {k: v['url'] for k, v in self.metadata.items() if not filters or any(s in v['url'] for s in filters)}
    #     n = len(urls)
    #     for i, (vid, url) in enumerate(urls.items()):
    #         print(f'Downloading video {i + 1} / {n}')
    #         print('Vid name: ', vid)
    #         print('URL: ', url)
    #         print('output_dir: ', output_dir)
    #         subprocess.call(['you-get', '-o', output_dir, '-O', vid, url])
    #         # subprocess.run(['you-get', '-o', output_dir, '-O', vid, url])
            

    def download(self, audio_output_dir, video_output_dir, filters=None):
        if not os.path.isdir(video_output_dir):
            os.makedirs(video_output_dir)
        if not os.path.isdir(audio_output_dir):
            os.makedirs(audio_output_dir)
        urls = {k: v['url'] for k, v in self.metadata.items() if not filters or any(s in v['url'] for s in filters)}
        n = len(urls)
        for i, (vid, url) in enumerate(urls.items()):
            print(f'Downloading video {i + 1} / {n}')
            # subprocess.call(['you-get', '-o', output_dir, '-O', vid, url])
            subprocess.run(['you-get', '-o', video_output_dir, '-O', vid, url])
            # Move file ending in [01] to audio section
            # https://stackabuse.com/how-to-create-move-and-delete-files-in-python/
            # os.rename
            for file in os.listdir(video_output_dir):
                resource = os.path.join(video_output_dir, file) 
                audio_name = vid+'[01]'
                video_name = vid+'[00]'
                if os.path.isfile(resource) and audio_name in file:
                    new_file = file.replace('[01]', '')
                    new_resource = os.path.join(audio_output_dir, new_file)
                    os.rename(resource, new_resource)
                elif os.path.isfile(resource) and video_name in file:
                    new_file = file.replace('[00]', '')
                    new_resource = os.path.join(video_output_dir, new_file)
                    os.rename(resource, new_resource)
                    
            

    def get_metadata(self, source, num, **kwargs):
        if source == Spider.BILIBILI:
            m = Bilibili()
        elif source == Spider.TENCENT:
            m = Tencent()
        elif source == Spider.IQIYI:
            m = Iqiyi()
        elif source == Spider.YOUKU:
            m = Youku()
        elif source == Spider.YOUTUBE:
            m = Youtube()
        else:
            print('Unknown source')
            return
        new_metadata = m.get_metadata(self.query, num, **kwargs)
        self.metadata.update(new_metadata)


class ChineseExtractor:
    def __init__(self):
        self.source = None

    @staticmethod
    def get_fs(query, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def extract_vids_and_urls(response):
        raise NotImplementedError()

    def get_metadata(self, query, num, **kwargs):
        result = {}
        fs = self.get_fs(query, **kwargs)
        page = 1
        count = 0
        while count < num:
            prev_count = count
            s = fs % page
            response = requests.get(s, headers=Spider.HEADER)
            if response.status_code != 200:
                print('Search failed: ' + s)
                return
            vids_and_urls = self.extract_vids_and_urls(response)
            for vid, url in vids_and_urls:
                print(f'--- Source {self.source}, Video {count + 1} / {num} ---')
                try:
                    metadata = self.get_metadata_from_url(url)
                except Exception as e:
                    print(f'Error: {url}')
                    print(e)
                    continue
                if not metadata:
                    continue
                result[vid] = metadata
                count += 1
                if count == num:
                    break
            if count == prev_count:
                break
            page += 1
        return result

    @staticmethod
    def get_metadata_from_url(url):
        raise NotImplementedError()


class Bilibili(ChineseExtractor):
    def __init__(self):
        super().__init__()
        self.source = Spider.BILIBILI

    @staticmethod
    def get_fs(query, duration=1, order=0, tids_1=0, tids_2=0, **kwargs):
        bilibili_orders = ['totalrank', 'click', 'pubdate', 'dm', 'stow']
        fs = f'https://search.bilibili.com/all?keyword={query}&order={bilibili_orders[order]}&' \
             f'duration={duration}&tids_1={tids_1}&tids_2={tids_2}&page=%d'
        return fs

    def extract_vids_and_urls(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        video_items = soup.find_all('li', {'class': 'video-item matrix'})
        vids = [v.find('a')['href'].rsplit('/', 1)[-1].split('?')[0]  for v in video_items]
        urls = ['https://www.bilibili.com/video/' + vid for vid in vids]
        return [*zip(vids, urls)]

    @staticmethod
    def get_metadata_from_url(url):
        response = requests.get(url, headers=Spider.HEADER)
        if response.status_code != 200:
            print('Video page failed: ' + url)
            return
        s = re.search(r'window.__INITIAL_STATE__=({.*?});', response.text).group(1)
        d = json.loads(s)['videoData']
        metadata = {'url': url, 'title': d['title'], 'description': d['desc'], 'duration': d['duration'],
                    'publish_time': datetime.fromtimestamp(d['pubdate']),
                    'last_time': datetime.fromtimestamp(d['ctime']), 'poster': d['owner']['name']}
        return metadata


class Tencent(ChineseExtractor):
    def __init__(self):
        super().__init__()
        self.source = Spider.TENCENT

    @staticmethod
    def get_fs(query, duration=1, **kwargs):
        fs = f'https://v.qq.com/x/search/?q={query}&cxt=%%3Dduration%%3D{duration}&cur=%d'
        return fs

    @staticmethod
    def extract_vids_and_urls(response):
        soup = BeautifulSoup(response.text, 'html.parser')
        video_items = soup.find_all('div', {'class': 'result_item result_item_h _quickopen'})
        urls = [v.a['href'] for v in video_items]
        vids = [re.search(r'/([^/]*?)\.html', url).group(1) for url in urls]
        return [*zip(vids, urls)]

    @staticmethod
    def get_metadata_from_url(url):
        response = requests.get(url, headers=Spider.HEADER)
        if response.status_code != 200:
            print('Video page failed: ' + url)
            return
        s = re.search(r'var\s*VIDEO_INFO\s*=\s*({.*?})[;\n]', response.text, re.DOTALL).group(1)
        d = json.loads(s)
        pt = d['publish_date']
        if pt and pt[0] != '0':
            if len(pt) > 10:
                publish_time = datetime.strptime(pt, '%Y-%m-%d %H:%M:%S')
            else:
                publish_time = datetime.strptime(pt, '%Y-%m-%d')
        else:
            publish_time = None
        lt = d['modify_time']
        if lt and lt[0] != '0':
            if len(lt) > 10:
                last_time = datetime.strptime(lt, '%Y-%m-%d %H:%M:%S')
            else:
                last_time = datetime.strptime(lt, '%Y-%m-%d')
        else:
            last_time = None
        metadata = {'url': url, 'title': d['title'], 'description': d['desc'], 'duration': int(d['duration']),
                    'publish_time': publish_time, 'last_time': last_time, 'poster': d['upload_qq']}
        return metadata


class Iqiyi(ChineseExtractor):
    def __init__(self):
        super().__init__()
        self.source = Spider.IQIYI

    @staticmethod
    def get_fs(query, duration=1, **kwargs):
        duration = duration + 1 if duration != 0 else 0
        fs = f'https://so.iqiyi.com/so/q_{query}_ctg__t_{duration + 1 if duration != 0 else 0}' + \
             '_page_%d_p_1_qc_0_rd__site_iqiyi_m_1_bitrate_'
        return fs

    @staticmethod
    def extract_vids_and_urls(response):
        vids = list(set(re.findall(r'/(._.*?)\.html', response.text)))
        urls = [f'https://www.iqiyi.com/{vid}.html' for vid in vids]
        return [*zip(vids, urls)]

    @staticmethod
    def get_metadata_from_url(url):
        response = requests.get(url, headers=Spider.HEADER)
        if response.status_code != 200:
            print('Video page failed: ' + url)
            return
        s = re.search(r'video-info=\'({.*?})\'', response.text).group(1)
        d = json.loads(s)
        poster = d['user']['name'] if 'user' in d else None
        metadata = {'url': url, 'title': d['name'], 'description': d['description'], 'duration': d['duration'],
                    'publish_time': datetime.fromtimestamp(d['firstPublishTime'] * 1e-3),
                    'last_time': datetime.fromtimestamp(d['lastPublishTime'] * 1e-3), 'poster': poster,
                    'subtitle': d['subtitle']}
        return metadata


class Youku(ChineseExtractor):
    def __init__(self):
        super().__init__()
        self.source = Spider.YOUKU

    @staticmethod
    def get_fs(query, duration=1, **kwargs):
        fs = f'https://so.youku.com/search_video/q_{query}?aaid=0&lengthtype={duration}&pg=%d'
        return fs

    @staticmethod
    def extract_vids_and_urls(response):
        vids = list(set(re.findall(r'(id_.*?)\.html', response.text)))
        urls = [f'https://v.youku.com/v_show/{vid}.html' for vid in vids]
        return [*zip(vids, urls)]

    @staticmethod
    def get_metadata_from_url(url):
        response = requests.get(url, headers=Spider.HEADER)
        if response.status_code != 200:
            print('Video page failed: ' + url)
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('meta', {'name': 'title'})['content']
        description = soup.find('meta', {'name': 'description'})['content']
        duration = round(float(re.search(r'seconds:\s*\'(.*?)\'', response.text).group(1)))
        pt = soup.find('meta', {'itemprop': 'datePublished'})['content']
        publish_time = datetime.strptime(pt, '%Y-%m-%d %H:%M:%S') if pt else None
        lt = soup.find('meta', {'itemprop': 'uploadDate'})['content']
        last_time = datetime.strptime(lt, '%Y-%m-%d %H:%M:%S') if lt else None
        poster = re.search(r'videoOwner:\s*\'(.*?)\'', response.text).group(1)
        metadata = {'url': url, 'title': title, 'description': description, 'duration': duration,
                    'publish_time': publish_time, 'last_time': last_time, 'poster': poster}
        return metadata


class Youtube:
    def __init__(self):
        self.source = Spider.YOUTUBE

    def get_metadata(self, query, num, key, duration=1):
        durations = ['short', 'medium', 'long', 'any']
        api_url = 'https://www.googleapis.com/youtube/v3/search'
        params = {'key': key, 'q': query, 'videoDuration': durations[duration], 'part': 'snippet', 'type': 'video',
                  'maxResults': 50}

        # params = {'key': query, 'q': key, 'videoDuration': durations[duration], 'part': 'snippet', 'type': 'video',
        #            'maxResults': 50}

        print("param: ",params)

        result = {}
        while len(result) < num:
            r = requests.get(api_url, params=params)
            if r.status_code != 200:
                print('Search failed: ' + api_url)
                return
            results_json = r.json()
            video_items = results_json['items']
            for v in video_items:
                if len(result) >= num:
                    break
                vid = v['id']['videoId']
                result[vid] = self.extract_metadata(v)
            print(f'--- Source {self.source}, Video {len(result)} / {num} ---')
            if 'nextPageToken' not in results_json:
                break
            params['pageToken'] = results_json['nextPageToken']
        return result

    @staticmethod
    def extract_metadata(video_item):
        url = 'https://www.youtube.com/watch?v=' + video_item['id']['videoId']
        snippet = video_item['snippet']
        publish_time = datetime.strptime(snippet['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        metadata = {'url': url, 'title': snippet['title'], 'description': snippet['description'],
                    'publish_time': publish_time, 'poster': snippet['channelTitle']}
        return metadata

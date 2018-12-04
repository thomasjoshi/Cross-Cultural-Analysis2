import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup


def get_responses(keyword, num, order=0, duration=0, tids_1=0, tids_2=0):
    orders = ('totalrank', 'click', 'pubdate', 'dm', 'stow')
    result = []
    page = 1
    while len(result) < num:
        s = 'https://search.bilibili.com/all?keyword=' + keyword + '&order=' + orders[order] + '&duration=' + str(
            duration) + '&tids_1=' + str(tids_1) + '&tids_2=' + str(tids_2) + '&page=' + str(page)
        response = requests.get(s)
        soup = BeautifulSoup(response.text, 'html.parser')
        video_items = soup.find_all('li', {'class': 'video matrix'})
        for v in video_items:
            url = 'https://www.bilibili.com/video/' + v.find('span', {'class': 'type avid'}).text
            resp = requests.get(url, headers={'User-Agent': 'Chrome/70.0.3538.110'})
            if resp.status_code == 200:
                result.append((url, resp))
                print('Got video %d / %d' % (len(result), num))
                if len(result) == num:
                    break
        page += 1
    return result


def parse(p):
    url, response = p
    l = None
    for line in response.text.split('\n'):
        if 'window.__INITIAL_STATE__=' in line:
            l = line[line.find('__INITIAL_STATE__='):]
            l = l[l.find('{'):]
            l = l[:1 + l.find('};')]
            break
    d = json.loads(l)['videoData']
    return {'url': url, 'title': d['title'], 'description': d['desc'], 'duration': d['duration'],
            'publish_time': datetime.fromtimestamp(d['pubdate']), 'last_time': datetime.fromtimestamp(d['ctime']),
            'poster': d['owner']['name'], 'id': d['aid']}

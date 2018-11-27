import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup


def get_responses(keyword, num):
    result = []
    page = 1
    while len(result) < num:
        s = 'https://v.qq.com/x/search/?q=' + keyword + '&cur=' + str(page)
        response = requests.get(s)
        soup = BeautifulSoup(response.text, 'html.parser')
        video_items = soup.find_all('div', {'class': 'result_item result_item_h _quickopen'})
        for v in video_items:
            url = v.a['href']
            resp = requests.get(url)
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
        if 'var VIDEO_INFO' in line:
            l = line[line.find('{'):]
            break
    d = json.loads(l)
    publish_time = datetime.strptime(d['publish_date'], '%Y-%m-%d %H:%M:%S') if d['publish_date'] is not None else None
    last_time = datetime.strptime(d['modify_time'], '%Y-%m-%d %H:%M:%S') if d['publish_date'] is not None else None
    return {'url': url, 'title': d['title'], 'description': d['desc'], 'duration': int(d['duration']), 'publish_time': publish_time, 'last_time': last_time, 'watches': int(d['view_all_count']), 'poster': d['upload_qq'], 'id': d['vid']}

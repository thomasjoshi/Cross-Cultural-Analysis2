import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup


def get_responses(keyword, num):
    result = []
    page = 1
    while len(result) < num:
        s = 'https://so.iqiyi.com/so/q_' + keyword + '_ctg__t_0_page_' + str(page) + '_p_1_qc_0_rd__site__m_1_bitrate_'
        response = requests.get(s)
        soup = BeautifulSoup(response.text, 'html.parser')
        video_items = soup.find_all('li', {'class': 'list_item'})
        for v in video_items:
            url = v.find({'a', 'href'})['href']
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
        if 'video-info' in line:
            l = line[line.find('video-info'):]
            l = l[l.find("'") + 1:]
            l = l[:l.find("'")]
            break
    d = json.loads(l)
    poster = d['user']['name'] if 'user' in d else None
    return {'url': url, 'title': d['name'], 'description': d['description'], 'duration': d['duration'], 'publish_time': datetime.fromtimestamp(d['firstPublishTime'] * 1e-3), 'last_time': datetime.fromtimestamp(d['lastPublishTime'] * 1e-3), 'poster': poster, 'id': d['vid'], 'subtitle': d['subtitle']}

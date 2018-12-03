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
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('meta', {'name': 'title'})['content']
    poster = soup.find('meta', {'name': 'author'})['content']
    description = soup.find('meta', {'name': 'description'})['content']
    duration = soup.find('meta', {'itemprop': 'duration'})['content']
    duration = int(duration) if duration.isnumeric() else None
    lt = soup.find('meta', {'itemprop': 'uploadDate'})['content']
    last_time = datetime.strptime(lt, '%Y-%m-%d %H:%M:%S') if len(lt) > 10 else datetime.strptime(lt, '%Y-%m-%d')
    pt = soup.find('meta', {'itemprop': 'datePublished'})['content']
    publish_time = datetime.strptime(pt, '%Y-%m-%d %H:%M:%S') if len(pt) > 10 else datetime.strptime(pt, '%Y-%m-%d')
    watches = int(soup.find('meta', {'itemprop': 'interactionCount'})['content'])
    return {'url': url, 'title': title, 'description': description, 'duration': duration,
            'publish_time': publish_time, 'last_time': last_time, 'watches': watches,
            'poster': poster}

    # url, response = p
    # l = response.text[response.text.find('var VIDEO_INFO'):]
    # l = l[l.find('{'):]
    # pos = l.find('};')
    # if pos == -1:
    #     pos = l.find('}\n')
    #     if pos == -1:
    #         return
    # l = l[:1 + pos]
    # d = json.loads(l)
    # publish_time = datetime.strptime(d['publish_date'], '%Y-%m-%d %H:%M:%S') if d['publish_date'] is not None else None
    # last_time = datetime.strptime(d['modify_time'], '%Y-%m-%d %H:%M:%S') if d['publish_date'] is not None else None
    # return {'url': url, 'title': d['title'], 'description': d['desc'], 'duration': int(d['duration']), 'publish_time': publish_time, 'last_time': last_time, 'watches': int(d['view_all_count']), 'poster': d['upload_qq'], 'id': d['vid']}

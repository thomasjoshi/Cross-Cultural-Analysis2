import requests
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError

youtube_api_key = 'AIzaSyCIoGnZWAmCR-8hPFNN4Sch7BgMEd0Hm6c'
q = 'alphago news us'
url = 'https://www.googleapis.com/youtube/v3/search'
params = {
    'q': 'alphago news us',
    'part': 'snippet',
    'key': youtube_api_key,
    'type': 'video',
    'maxResults': 50
}

r = requests.get(url, params=params)
results_json = r.json()

next_page_token = ''
results = []
for i in range(10):
    params['pageToken'] = next_page_token
    r = requests.get(url, params=params)
    results_json = r.json()
    results += results_json['items']
    if 'nextPageToken' in results_json:
        print(results_json['nextPageToken'])
        next_page_token = results_json['nextPageToken']
    else:
        break

prefix = 'https://www.youtube.com/watch?v='
videolist = [prefix + result['id']['videoId'] for result in results]


def modify_filename(filename):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in filename if c in valid_chars)


n = 0
for item in videolist:
    n += 1
    try:
        print (item)
        yt = YouTube(item)
        print (n, yt.title)
        if int(yt.length) > 300:
            continue
        video = yt.streams.filter(type="video").all()[0]
        print ('Downloading ' + str(n) + '...')
        path = './videos/alphago_news_us/'
        video.download(output_path=path, filename="%d_%s" % (n, modify_filename(video.default_filename)))
    except (VideoUnavailable, RegexMatchError, IndexError, UnboundLocalError):
        continue
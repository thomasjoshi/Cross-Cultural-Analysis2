# Cross_Cultural_Analysis

## Prerequisites
* Install `ffmpeg` for video extraction
    * Linux (Ubuntu): `sudo apt install ffmpeg`
* Install python packages
    * `pip install -r requirements.txt`
    * `pip install tensorflow`
* API key
    * [Google YouTube API](https://developers.google.com/youtube/v3)

## TODO
* `find_topics.py` line 92, need both vo and ao
* `spider.py` line 252, `fs = f'https://so.iqiyi.com/so/q_{query}'`
* Should **NOT** print API key for security purpose
* `get_metadata.py` `try except`
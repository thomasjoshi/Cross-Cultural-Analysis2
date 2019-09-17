#!/usr/bin/env bash
python3 get_metadata.py "alphago" -o ../metadata/alphago
python3 download_videos.py ../metadata/alphago/data -o ../videos/alphago/bilibili -s bilibili

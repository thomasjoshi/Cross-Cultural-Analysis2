#!/usr/bin/env bash
python3 run_parser.py "alphago" -o ../metadata/alphago
python3 download.py ../metadata/alphago/data -o ../videos/alphago/bilibili -s bilibili
python3 count.py ../metadata/alphago/titles.txt -o ../counts/alphago/titles_counts.txt -p ../counts/alphago/titles_counts.png
python3 count.py ../metadata/alphago/descriptions.txt -o ../counts/alphago/descriptions_counts.txt -p ../counts/alphago/descriptions_counts.png

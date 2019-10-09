#!/usr/bin/env bash
src="$(dirname $0)/src"
results="$(dirname $0)/results"

# get video metadata
python3 $src/spidering/get_metadata.py "AlphaGo" -n 2 -o $results/AlphaGo/chinese/video_metadata -s bilibili qq iqiyi youku
python3 $src/spidering/get_metadata.py "AlphaGo" -n 2 -o $results/AlphaGo/english/video_metadata -s youtube -k key.txt

# download videos
python3 $src/spidering/download.py $results/AlphaGo/chinese/video_metadata/metadata -o $results/AlphaGo/chinese/videos -s bilibili
python3 $src/spidering/download.py $results/AlphaGo/english/video_metadata/metadata -o $results/AlphaGo/english/videos -s youtube

# analysis
python3 $src/analysis/count_words_cn.py $results/AlphaGo/chinese/video_metadata/titles.txt -o $results/AlphaGo/chinese/video_metadata/titles_wordcounts.txt -p $results/AlphaGo/chinese/video_metadata/titles_wordcounts.png
python3 $src/analysis/trend.py -i $results/topics_trend/topics_2018_US.json -d $results/topics_trend/topics.txt -o $results/topics_trend/topics_data -p "AlphaGo"

# dataset
python3 $src/dataset/extract_audio.py $results/AlphaGo/chinese/videos -o $results/AlphaGo/chinese/audios
python3 $src/dataset/extract_audio.py $results/AlphaGo/english/videos -o $results/AlphaGo/english/audios

python3 $src/dataset/extract_transcript.py $results/AlphaGo/chinese/audios key.json cross-culture-audios-stanley -o $results/AlphaGo/chinese/transcripts -l cmn-Hans-CN -d audios_cn -t "AlphaGo" "AlphaZero" "DeepMind"
python3 $src/dataset/extract_transcript.py $results/AlphaGo/english/audios key.json cross-culture-audios-stanley -o $results/AlphaGo/english/transcripts -l en-US -d audios_en -t "AlphaGo" "Lee Sedol" "Ke Jie"

python3 $src/dataset/extract_frame.py $results/AlphaGo/chinese/transcripts $results/AlphaGo/chinese/videos -o $results/AlphaGo/chinese/frames -d $results/AlphaGo/chinese/image_text_pairs
python3 $src/dataset/extract_frame.py $results/AlphaGo/english/transcripts $results/AlphaGo/english/videos -o $results/AlphaGo/english/frames -d $results/AlphaGo/english/image_text_pairs

#python find_duplicate.py --dataset AlphaGo --feature_format npy --threshold 0.1

#python filter_ads.py --dataset AlphaGo --folder chinese --blacklist_threshold 30 --whitelist_threshold 20

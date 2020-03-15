#!/usr/bin/env bash
src="$(dirname $0)/src"
results="$(dirname $0)/results"

echo "##############################################"
echo "find topics"
echo "##############################################"
python3 $src/analysis/find_topics.py $results/find_topics/topics_cn.txt  $results/find_topics/topics_en.txt key.txt -o $results/find_topics -n 1 -f 10

echo "##############################################"
echo "get video metadata"
echo "##############################################"
python3 $src/spidering/get_metadata.py "AlphaGo" -n 1 -o $results/AlphaGo/chinese/video_metadata -s bilibili qq iqiyi youku
python3 $src/spidering/get_metadata.py "AlphaGo" -n 1 -o $results/AlphaGo/english/video_metadata -s youtube -k key.txt

echo "##############################################"
echo "download videos"
echo "##############################################"
python3 $src/spidering/download.py $results/AlphaGo/chinese/video_metadata/metadata -o $results/AlphaGo/chinese/videos -s bilibili
python3 $src/spidering/download.py $results/AlphaGo/english/video_metadata/metadata -o $results/AlphaGo/english/videos -s youtube

echo "##############################################"
echo "analysis"
echo "##############################################"
python3 $src/analysis/count_words_cn.py $results/AlphaGo/chinese/video_metadata/titles.txt -o $results/AlphaGo/chinese/video_metadata/titles_wordcounts.txt -p $results/AlphaGo/chinese/video_metadata/titles_wordcounts.png
python3 $src/analysis/trend.py -i $results/topics_trend/topics_2018_US.json -d $results/topics_trend/topics.txt -o $results/topics_trend/topics_data -p "AlphaGo"

echo "##############################################"
echo "dataset extect audios"
echo "##############################################"
python3 $src/dataset/extract_audio.py $results/AlphaGo/chinese/videos -o $results/AlphaGo/chinese/audios
python3 $src/dataset/extract_audio.py $results/AlphaGo/english/videos -o $results/AlphaGo/english/audios

echo "##############################################"
echo "dataset extract transcripts"
echo "##############################################"
python3 $src/dataset/extract_transcript.py $results/AlphaGo/chinese/audios key.json cross-culture-audios-stanley -o $results/AlphaGo/chinese/transcripts -l cmn-Hans-CN -d audios_cn -t "AlphaGo" "AlphaZero" "DeepMind"
python3 $src/dataset/extract_transcript.py $results/AlphaGo/english/audios key.json cross-culture-audios-stanley -o $results/AlphaGo/english/transcripts -l en-US -d audios_en -t "AlphaGo" "Lee Sedol" "Ke Jie"

echo "##############################################"
echo "dataset process transcript"
echo "##############################################"
python3 $src/dataset/process_transcript.py $results/AlphaGo/chinese/transcripts -o $results/AlphaGo/chinese/processed_transcript.json
python3 $src/dataset/process_transcript.py $results/AlphaGo/english/transcripts -o $results/AlphaGo/english/processed_transcript.json

echo "##############################################"
echo "dataset extract frame"
echo "##############################################"
python3 $src/dataset/extract_frame.py $results/AlphaGo/chinese/processed_transcript.json $results/AlphaGo/chinese/videos -o $results/AlphaGo/chinese/frames -d $results/AlphaGo/chinese/image_text_pairs
python3 $src/dataset/extract_frame.py $results/AlphaGo/english/processed_transcript.json $results/AlphaGo/english/videos -o $results/AlphaGo/english/frames -d $results/AlphaGo/english/image_text_pairs


echo "##############################################"
echo "dataset extract features"
echo "##############################################"
python3 $src/dataset/extract_feature.py $results/AlphaGo/chinese/image_text_pairs -o $results/AlphaGo/chinese/features_data
python3 $src/dataset/extract_feature.py $results/AlphaGo/english/image_text_pairs -o $results/AlphaGo/english/features_data

echo "##############################################"
echo "dataset find duplicate"
echo "##############################################"
python3 $src/dataset/find_duplicate.py $results/AlphaGo/chinese/features_data $results/AlphaGo/english/features_data -o $results/AlphaGo/pairs.json -t 0.25 -d angular

#python filter_ads.py --dataset AlphaGo --folder chinese --blacklist_threshold 30 --whitelist_threshold 20

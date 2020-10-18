#!/usr/bin/env bash
src="$(dirname $0)/src"
results="$(dirname $0)/results"

echo "##############################################"
echo "get video metadata"
echo "##############################################"
# python3 $src/spidering/get_metadata.py "AlphaGo" -n 1 -o $results/AlphaGo/chinese/video_metadata -s bilibili qq youku
# python3 $src/spidering/get_metadata.py "AlphaGo" -n 4 -o $results/AlphaGo/english/video_metadata -s youtube -k key.txt

echo "##############################################"
echo "download videos"
echo "##############################################"
# python3 $src/spidering/download.py $results/AlphaGo/chinese/video_metadata/metadata -ao $results/AlphaGo/chinese/audios -vo $results/AlphaGo/chinese/videos -s bilibili qq youku
# python3 $src/spidering/download.py $results/AlphaGo/english/video_metadata/metadata -ao $results/AlphaGo/english/audios -vo $results/AlphaGo/english/videos -s youtube

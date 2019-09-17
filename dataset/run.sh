#!/usr/bin/env bash
#python split_audio_video.py --rename 1 --split 1 --dataset AlphaGo --folder english
#python split_audio_video.py --rename 1 --split 1 --dataset AlphaGo --folder chinese

#python speech_recognition.py --dataset AlphaGo --folder chinese --gs_dest audios_chi
#python speech_recognition.py --dataset AlphaGo --folder english --gs_dest audios_eng

#python extract_frame.py --dataset AlphaGo --folder chinese

#python find_duplicate.py --dataset AlphaGo --feature_format npy --threshold 0.1

python filter_ads.py --dataset AlphaGo --folder chinese --blacklist_threshold 30 --whitelist_threshold 20

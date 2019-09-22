#!/usr/bin/env bash
python3 extract_audio.py AlphaGo/chinese/videos -o AlphaGo/chinese/audios
python3 extract_audio.py AlphaGo/english/videos -o AlphaGo/english/audios

python3 extract_transcript.py AlphaGo/chinese/audios key.json cross-culture-audios-stanley -o AlphaGo/chinese/transcripts -l cmn-Hans-CN -d audios_cn -t "AlphaGo" "AlphaZero" "DeepMind"
python3 extract_transcript.py AlphaGo/english/audios key.json cross-culture-audios-stanley -o AlphaGo/english/transcripts -l en-US -d audios_en -t "AlphaGo" "Lee Sedol" "Ke Jie"

#python extract_frame.py --dataset AlphaGo --folder chinese

#python find_duplicate.py --dataset AlphaGo --feature_format npy --threshold 0.1

python filter_ads.py --dataset AlphaGo --folder chinese --blacklist_threshold 30 --whitelist_threshold 20

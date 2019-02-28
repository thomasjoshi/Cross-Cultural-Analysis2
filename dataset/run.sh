#python transcode.py --rename 1 --split 1 --dataset AlphaGo --folder english
#python transcode.py --rename 1 --split 1 --dataset AlphaGo --folder chinese

python transcribe.py --dataset AlphaGo --folder chinese --gs_dest audios_chi
python transcribe.py --dataset AlphaGo --folder english --gs_dest audios_eng

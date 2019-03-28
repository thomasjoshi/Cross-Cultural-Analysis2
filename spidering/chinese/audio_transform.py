from subprocess import Popen, run
from os import walk, system
from os.path import splitext

def sort_file(filename):
    return int(filename.split('_')[0])

def convert_to_flac():
    for (root, dirs, files) in walk('./audios/alphago_news_us'):
        p = []
        for file in files:
            new_file = splitext(file)[0] + '.flac'
            command = 'ffmpeg -i "./audios/alphago_news_us/%s" -ac 1 "./audios/alphago_news_us_flac/%s"' % (file, new_file)
            system(command)

from speech_to_text import Translator
translator = Translator()

for (root, dirs, files) in walk ('./audios/alphago_news_us_flac'):
    files.sort(key=lambda file: sort_file(file))
    for filename in files[:1]:
        print ('Translating %s...' % filename)
        gs_uri = translator.upload_to_gcs('./audios/alphago_news_us_flac/%s' % filename)
        results = translator.translate_long(gs_uri)
        translator.delete_from_gcs(filename)
        text_file = splitext(filename)[0] + '.txt'
        with open('./audios/alphago_news_us_text/%s' % (text_file), 'w+') as f:
            f.write(results)

import json
for (root, dirs, files) in walk ('./audios/alphago_news_us_flac/'):
    files.sort(key=lambda file: sort_file(file))
    n = 5
    for filename in files[n:]:
        print ('%d Translating %s...' % (n, filename))
        gs_uri = translator.upload_to_gcs('./audios/alphago_news_us_flac/%s' % filename)
        results = translator.translate_with_timestamps(gs_uri)
        translator.delete_from_gcs(filename)
        json_file = splitext(filename)[0] + '.json'
        with open('./audios/alphago_news_us_text_timestamps/%s' % (json_file), 'w+') as f:
            json.dump(results, f)

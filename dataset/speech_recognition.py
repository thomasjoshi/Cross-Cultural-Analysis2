#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import ntpath
import argparse
from os import walk
from google.cloud.speech_v1p1beta1 import types, SpeechClient
from google.cloud import storage

parser = argparse.ArgumentParser(description='Transcribe: convert audio file into text')
parser.add_argument('--folder', type=str, default="english", help='language of the transcript')
parser.add_argument('--dataset', type=str, default="AlphaGo", help='name of the news event')
parser.add_argument('--audio_format', type=str, default=".flac", help='format of output audios')
parser.add_argument('--gs_bucket', type=str, default="cross-culture-audios-stanley", help='google cloud storage bucket')
parser.add_argument('--gs_dest', type=str, default="audios", help='google cloud storage folder for audio files')
parser.add_argument('--threshold', type=float, default=0.85, help='threshold for dropping unconfident transcripts')
opt = parser.parse_args()

dataset_name = "./" + opt.dataset
dataset_path = dataset_name + "/" + opt.folder
audio_path = dataset_path + "/audios"
transcript_path = dataset_path + "/transcripts"

audio_type = opt.audio_format

if opt.folder == "english":
    mode = 'en-US'
    hint = ['AlphaGo', 'Lee Sedol', 'Ke Jie']
elif opt.folder == 'chinese':
    mode = 'cmn-Hans-CN'
    hint = ['AlphaGo','AlphaZero', 'DeepMind']
else:
    print('Error: Need to specify the language for google speech recognition...')

if not os.path.exists(audio_path):
    os.makedirs(audio_path)

if not os.path.exists(transcript_path):
    os.makedirs(transcript_path)

class Transcriber:
    def __init__(self):
        self.client = SpeechClient()
        storage_client = storage.Client()
        self.bucket_name = opt.gs_bucket
        self.bucket = storage_client.get_bucket(self.bucket_name)

    def translate_with_timestamps(self, gs_uri):
        audio = types.RecognitionAudio(
            uri=gs_uri,
        )
        config = types.RecognitionConfig(
            encoding='FLAC',
            language_code= mode,
            enable_word_time_offsets=True,
            speech_contexts=[types.SpeechContext(
            phrases=hint,
           )],
            enable_word_confidence=True
        )
        operation = self.client.long_running_recognize(config=config, audio=audio)
        results = []
        for result in operation.result().results:
            alternatives = result.alternatives
            if len(alternatives) == 0:
                continue
            alternative = alternatives[0]
            results.append([alternative.transcript, alternative.confidence])
            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time.seconds + round(word_info.start_time.nanos * 1e-9, 1)
                end_time = word_info.end_time.seconds + round(word_info.end_time.nanos * 1e-9, 1)
                confidence = round(word_info.confidence,4)
                results.append([word, start_time, end_time, confidence])
        return results

    def upload_to_gcs(self, filepath):
        filename = ntpath.basename(filepath)
        gs_filepath = opt.gs_dest + '/' + filename
        blob = self.bucket.blob(gs_filepath)
        blob.upload_from_filename(filepath)
        return self.generate_uri(gs_filepath)

    def delete_from_gcs(self, filename):
        gs_filepath = opt.gs_dest + '/' + filename
        self.bucket.delete_blob(gs_filepath)

    def generate_uri(self, filepath):
        return 'gs://%s/%s' % (self.bucket_name, filepath)

if __name__ == '__main__':
    transcriber = Transcriber()
    f_log = open('log.txt', 'w')

    a_list = []
    for (dirpath, dirnames, filenames) in walk(audio_path):
        a_list.extend(filenames)

    for index,audio_filename in enumerate(a_list):
        trans_file = transcript_path + '/' + audio_filename[:-len(audio_type)] + '.txt'
        if os.path.isfile(trans_file):
            continue
        if audio_filename[-len(audio_type):] == audio_type and audio_filename[0] != '.':
            print('===> Start uploding file: ' + audio_filename)
            gs_uri = transcriber.upload_to_gcs(audio_path + '/' + audio_filename)
            print('===> Finish uploading file: ' + audio_filename)

            try:
                results = transcriber.translate_with_timestamps(gs_uri)
                with open(transcript_path + '/' + audio_filename[:-len(audio_type)] + '.txt', 'w') as f:
                    for item in results:
                        if len(item) == 4:
                            word,start_time,end_time,confidence  = item[0],item[1], item[2], item[3]
                            if opt.folder == 'english':
                                f.write((word+"\t{}\t{}\t{}\n".format(start_time,end_time,confidence)))
                            else:
                                f.write((word.encode('utf-8')+"\t{}\t{}\t{}\n".format(start_time,end_time,confidence)))
                        else:
                            trans,confidence = item[0], item[1]
                            if confidence < opt.threshold:
                                print("===> Confidence value too low, dropping this transcript")
                                raise Exception('Confidence value too low!')

                            if opt.folder == 'english':
                                f.write((trans+"\t{}\n".format(confidence)))
                                print("--------------------------- transcript ---------------------------")
                                print(trans)
                            else:
                                f.write((trans.encode('utf-8')+"\t{}\n".format(confidence)))
                                print("--------------------------- transcript ---------------------------")
                                print(trans.encode('utf-8'))

                            print("--------------------------- confidence ---------------------------")
                            print(confidence)
                            print("--------------------------- confidence ---------------------------")
                            f.write("\n")
                f.close()

            except Exception as e:
                print("===> Error: writing to log.txt...")
                f_log.write(audio_filename)
                f_log.write(str(e))
                f_log.write('\n')

            print('===> Delete file: ' + audio_filename)
            transcriber.delete_from_gcs(audio_filename)

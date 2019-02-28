import os
import ntpath
import argparse
from os import walk
from google.cloud.speech_v1p1beta1 import types, SpeechClient
from google.cloud import storage

parser = argparse.ArgumentParser(description='Transcribe: convert audio file to ranscripts')
parser.add_argument('--folder', type=str, default="english", help='language of the transcript')
parser.add_argument('--dataset', type=str, default="AlphaGo", help='name of the news event')
parser.add_argument('--audio_format', type=str, default=".flac", help='format of output audios')
opt = parser.parse_args()

dataset_name = "./" + opt.dataset
dataset_path = dataset_name + "/" + opt.folder
audio_path = dataset_path + "/audios"
transcript_path = dataset_path + "/transcripts"

audio_type = opt.audio_format

if opt.folder == "english":
    mode = 'en-US'
elif opt.folder == 'chinese':
    mode = 'cmn-Hans-CN'
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
        self.bucket_name = 'cross-culture-audios-stanley'
        self.bucket = storage_client.get_bucket(self.bucket_name)

    def translate_with_timestamps(self, gs_uri):
        audio = types.RecognitionAudio(
            uri=gs_uri,
        )
        config = types.RecognitionConfig(
            encoding='FLAC',
            language_code= mode,
            enable_word_time_offsets=True,
            enable_word_confidence=True
        )
        operation = self.client.long_running_recognize(config=config, audio=audio)
        results = []
        for result in operation.result().results:
            alternatives = result.alternatives
            if len(alternatives) == 0:
                continue
            alternative = alternatives[0]
            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time.seconds + round(word_info.start_time.nanos * 1e-9, 1)
                end_time = word_info.end_time.seconds + round(word_info.end_time.nanos * 1e-9, 1)
                confidence = round(word_info.confidence,4)
                results.append([word, start_time, end_time, confidence])
        return results

    def upload_to_gcs(self, filepath):
        filename = ntpath.basename(filepath)
        gs_filepath = 'audios/%s' % filename
        blob = self.bucket.blob(gs_filepath)
        blob.upload_from_filename(filepath)
        return self.generate_uri(gs_filepath)

    def delete_from_gcs(self, filename):
        gs_filepath = 'audios/%s' % filename
        self.bucket.delete_blob(gs_filepath)

    def generate_uri(self, filepath):
        return 'gs://%s/%s' % (self.bucket_name, filepath)

if __name__ == '__main__':
    transcriber = Transcriber()

    a_list = []
    for (dirpath, dirnames, filenames) in walk(audio_path):
        a_list.extend(filenames)

    for index,audio_filename in enumerate(a_list):
        if audio_filename[-5:] == audio_type and audio_filename[0] != '.':
            print('===> Start uploding file: ' + audio_filename)
            gs_uri = transcriber.upload_to_gcs(audio_path + '/' + audio_filename)
            print('===> Finish uploading file: ' + audio_filename)
            results = transcriber.translate_with_timestamps(gs_uri)

            with open(transcript_path + '/' + audio_filename[:-5] + '.txt', 'w') as f:
                for item in results:
                    word,start_time,end_time,confidence  = item[0], item[1], item[2], item[3]
                    if opt.folder == 'english':
                        #f.write(word + '\t' + str(start_time) + '\t' + str(end_time) + '\t' + str(confidence) + '\n')
                        f.write(word+"\t{}\t{}\t{}\n".format((start_time,end_time,confidence)))
                    else:
                        f.write((word.encode('utf-8')+"\t{}\t{}\t{}\n".format(start_time,end_time,confidence)))
                        #f.write(word.encode('utf-8') + '\t' + str(start_time) + '\t' + end_time + '\t' + confidence + '\n')
            f.close()

            print('===> Delete file: ' + audio_filename)
            transcriber.delete_from_gcs(audio_filename)

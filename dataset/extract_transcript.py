#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import ntpath
import argparse
from google.cloud.speech_v1p1beta1 import types, SpeechClient
from google.cloud import storage


class Transcriber:
    def __init__(self, gs_bucket, gs_dir):
        self.gs_bucket = gs_bucket
        self.gs_dir = gs_dir
        self.client = SpeechClient()
        self.bucket = storage.Client().get_bucket(gs_bucket)

    def translate_with_timestamps(self, gs_uri, encoding, mode, hint):
        audio = types.RecognitionAudio(uri=gs_uri)
        config = types.RecognitionConfig(
            encoding=encoding,
            language_code=mode,
            enable_word_time_offsets=True,
            speech_contexts=[types.SpeechContext(phrases=hint)],
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
                confidence = round(word_info.confidence, 4)
                results.append([word, start_time, end_time, confidence])
        return results

    def upload_to_gcs(self, audio_path):
        audio_filename = ntpath.basename(audio_path)
        gs_path = os.path.join(self.gs_dir, audio_filename)
        self.bucket.blob(gs_path).upload_from_filename(audio_path)
        return self.generate_uri(gs_path)

    def delete_from_gcs(self, audio_filename):
        gs_path = os.path.join(self.gs_dir, audio_filename)
        self.bucket.delete_blob(gs_path)

    def generate_uri(self, gs_path):
        return 'gs://' + os.path.join(self.gs_bucket, gs_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract transcripts from audios')
    parser.add_argument('input', help='directory of audios to process')
    parser.add_argument('key', help='key file for google cloud api')
    parser.add_argument('gs_bucket', type=str, help='google cloud storage bucket')
    parser.add_argument('-o', '--output', default='transcripts', help='directory of transcripts to output')
    parser.add_argument('-l', '--language', default='en-US', help='language of audios')
    parser.add_argument('-f', '--audio-format', default='flac', help='audios format')
    parser.add_argument('-d', '--gs-dir', type=str, default='audios',
                        help='google cloud storage directory for audio files')
    parser.add_argument('-s', '--threshold', type=float, default=0.85,
                        help='threshold for dropping unconfident transcripts')
    parser.add_argument('-t', '--hint', nargs='*', help='hint words for speech recognition')
    args = parser.parse_args()

    transcript_type = 'txt'
    audio_dir = args.input
    key_file = args.key
    gs_bucket = args.gs_bucket
    transcript_dir = args.output
    mode = 'cmn-Hans-CN' if args.language[0].lower() == 'c' else 'en-US'
    audio_type = args.audio_format
    gs_dir = args.gs_dir
    threshold = args.threshold
    hint = args.hint if args.hint else []

    if not os.path.exists(transcript_dir):
        os.makedirs(transcript_dir)

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_file
    transcriber = Transcriber(gs_bucket, gs_dir)
    with open(os.path.join(transcript_dir, 'error_log.txt'), 'w') as f_log:
        for audio_filename in os.listdir(audio_dir):
            audio_path = os.path.join(audio_dir, audio_filename)
            if not (audio_filename.endswith('.' + audio_type) and os.path.isfile(audio_path)):
                continue
            dot_pos = audio_filename.rfind('.')
            transcript_filename = audio_filename[:dot_pos] + '.' + transcript_type
            transcript_path = os.path.join(transcript_dir, transcript_filename)
            if os.path.isfile(transcript_path):
                continue

            print('===> Start uploding file: ' + audio_filename)
            gs_uri = transcriber.upload_to_gcs(audio_path)
            print('===> Finish uploading file: ' + audio_filename)
            try:
                results = transcriber.translate_with_timestamps(gs_uri, audio_type.upper(), mode, hint)
                with open(transcript_path, 'w') as f:
                    skip = False
                    first = True
                    for item in results:
                        if len(item) == 2:
                            trans, confidence = item
                            if confidence < threshold:
                                print('===> Confidence value too low, dropping this transcript')
                                skip = True
                                continue
                            if not first:
                                f.write('\n')
                            else:
                                first = False
                            if skip:
                                skip = False
                            f.write(f'{trans}\t{confidence}\n')
                            print('--------------------------- transcript ---------------------------')
                            print(trans)
                            print('--------------------------- confidence ---------------------------')
                            print(confidence)
                        elif not skip:
                            word, start_time, end_time, confidence = item
                            f.write(f'{word}\t{start_time}\t{end_time}\t{confidence}\n')
            except Exception as e:
                print('===> Error: writing log...')
                f_log.write(audio_filename + str(e) + '\n')
            print('===> Delete file: ' + audio_filename)
            transcriber.delete_from_gcs(audio_filename)

import ntpath
from google.cloud.speech import types, SpeechClient
from google.cloud import storage

class Translator:
    def __init__(self):
        self.client = SpeechClient()
        storage_client = storage.Client()
        self.bucket_name = 'cross-culture-audios'
        self.bucket = storage_client.get_bucket(self.bucket_name)

    def translate_long(self, gs_uri):
        audio = types.RecognitionAudio(
            uri=gs_uri,
        )
        config = types.RecognitionConfig(
            encoding='FLAC',
            language_code='en-US',
            sample_rate_hertz=44100,
        )
        operation = self.client.long_running_recognize(config=config, audio=audio)
        op_result = operation.result()
        result = '\n'.join([str.strip(result.alternatives[0].transcript) for result in op_result.results if
                            len(result.alternatives) > 0])
        return result

    def translate_with_timestamps(self, gs_uri):
        audio = types.RecognitionAudio(
            uri=gs_uri,
        )
        config = types.RecognitionConfig(
            encoding='FLAC',
            language_code='en-US',
            # sample_rate_hertz=44100,
            enable_word_time_offsets=True
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
                results.append([word, start_time, end_time])
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
    translator = Translator()
    filename = 'harvard.flac'
    gs_uri = translator.upload_to_gcs(filename)
    # results = translator.translate_long(gs_uri)
    results = translator.translate_with_timestamps(gs_uri)
    print(results)
    translator.delete_from_gcs(filename)
    # print(results)
    # from os.path import splitext
    # text_file = splitext(filename)[0] + '.txt'
    # with open('./audios/alphago_news_us_text/%s' % (text_file), 'w+') as f:
    #     f.write(results)

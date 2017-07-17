import os
import boto3
from .config import key_id, aws_secret_access_key, region_name, sample_rate
from pygame import mixer, time


class Speech:
    """
    handles AWS poly TTS
    """

    def __init__(self):
        real_path = os.path.realpath(__file__)
        dir_path = os.path.dirname(real_path)+"/"
        self.file_name = dir_path+'polly_stream.ogg'

        self.polly_service = boto3.client(
            'polly',
            aws_access_key_id=key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def print_voice(self):
        r_voices = self.polly_service.describe_voices(
            LanguageCode='de-DE'
        )
        for voice in r_voices['Voices']:
            print(voice)
            print(voice['Id'])

    def request_polly(self, text, text_type='text'):
        polly_response = self.polly_service.synthesize_speech(
            OutputFormat='ogg_vorbis',
            SampleRate=str(sample_rate),
            Text=text,
            TextType=text_type,
            VoiceId='Vicki'
        )

        try:
            os.remove(self.file_name)
        except OSError:
            pass

        with open(self.file_name, 'wb') as f:
            f.write(polly_response['AudioStream'].read())

    def speak(self):
        mixer.init(frequency=sample_rate)
        mixer.music.load(self.file_name)
        mixer.music.play()

        while mixer.music.get_busy():
            time.Clock().tick(10)

#-*-coding:utf-8-*-
import os
import wave
import pyaudio

CHUNK = 1024

class Speaker(object):

    def __init__(self):
        self._audio = pyaudio.PyAudio()
    
    def finish(self):
        self._audio.terminate()

    def say(self, file_name):
        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data/_secret_wav",
            "{}.wav".format(file_name)
        )
        print(file_path)
        wf = wave.open(file_path, 'rb')

        stream = self._audio.open(
            format=self._audio.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)

        data = wf.readframes(CHUNK)

        while data != '':
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()
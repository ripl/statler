import sys
import wave

import pyaudio
import whisper


class Speech2text:

    def __init__(self) -> None:
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1 if sys.platform == 'darwin' else 2
        self.rate = 44100
        self.wav_name = 'cap_demo.wav'
        self.model = whisper.load_model("tiny")

    def record_and_transcribe(self, record_seconds=6):

        # record
        with wave.open(self.wav_name, 'wb') as wf:
            p = pyaudio.PyAudio()
            wf.setnchannels(self.channels)
            wf.setsampwidth(p.get_sample_size(self.format))
            wf.setframerate(self.rate)

            stream = p.open(format=self.format, channels=self.channels, rate=self.rate, input=True)

            print('Recording ...')
            for _ in range(0, self.rate // self.chunk * record_seconds):
                wf.writeframes(stream.read(self.chunk))
            print('Recording Done')

            stream.close()
            p.terminate()

        # transcribe
        result = self.model.transcribe("cap_demo.wav")
        print('recording text: ', result['text'])

        return result['text']

if __name__ == '__main__':
    speech2text = Speech2text()
    speech2text.record_and_transcribe()



# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 1 if sys.platform == 'darwin' else 2
# RATE = 44100
# RECORD_SECONDS = 6

# with wave.open('cap_demo.wav', 'wb') as wf:
#     p = pyaudio.PyAudio()
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(p.get_sample_size(FORMAT))
#     wf.setframerate(RATE)

#     stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

#     print('Recording...')
#     for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
#         wf.writeframes(stream.read(CHUNK))
#     print('Done')

#     stream.close()
#     p.terminate()

# model = whisper.load_model("tiny")
# result = model.transcribe("cap_demo.wav")
# print(result["text"])
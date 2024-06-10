import re

import speech_recognition as sr

from cap.helpers.speaker import Speaker
from cap.helpers import logger


def is_subseq(s1, s2):
    """ determine whether s1 is a subsequence of s2 """
    def is_subseq_(i, j):
        """ determine whether s1[:i] is a subsequence of s2[:j] """
        if not i:
            return True
        if i > j:
            return False
        if s1[i - 1] == s2[j - 1]:
            return is_subseq_(i - 1, j - 1)
        return is_subseq_(i, j - 1)
    return is_subseq_(len(s1), len(s2))


def should_wakeup(text):
    """ wake up if text is close to 'hey robot' """
    r = re.fullmatch('(.+?) (.+)', text)
    return r and r[1][0] == 'h' and is_subseq('rbt', r[2])


class Listener:
    def __init__(self) -> None:
        self.r = sr.Recognizer()
        # self.r.energy_threshold = 1000
        self.r.dynamic_energy_ratio = 2.5
        self.mic = sr.Microphone()
        with self.mic as mic:
            self.r.adjust_for_ambient_noise(mic, duration=3)

    def listen(self):
        with self.mic as mic:
            mic.stream.pyaudio_stream.stop_stream()
            print('========= I am ready!! ==============')
            Speaker.say('I\'m ready')
            while True:
                mic.stream.pyaudio_stream.start_stream()
                audio = self.r.listen(mic, phrase_time_limit=2)
                mic.stream.pyaudio_stream.stop_stream()
                text = self.r.recognize_whisper(audio)
                print(text, f'{self.r.energy_threshold:.0f}')
                if should_wakeup(text.strip().lower()):
                    Speaker.say('Hi!')
                    mic.stream.pyaudio_stream.start_stream()
                    audio = self.r.listen(mic, phrase_time_limit=16)
                    mic.stream.pyaudio_stream.stop_stream()
                    yield self.r.recognize_whisper(audio, translate='english')


class DummyListener:
    def listen(self, queries):
        for query in queries:
            import time
            logger.info('Waiting for 1 sec...')
            time.sleep(1)
            logger.info('Yielding query', query)
            yield query



if __name__ == '__main__':
    listen = Listener().listen()
    while True:
        text = next(listen)
        if text:
            Speaker.say(f'You just said {text}.')
        else:
            Speaker.say(f'Sorry, I can\'t hear you.')

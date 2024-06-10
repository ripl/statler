from io import BytesIO
from time import sleep

import pygame
from gtts import gTTS


class Speaker:
    pygame.mixer.init()

    def say(text, savefile=None, block=False):
        speech = gTTS(text)
        fp = BytesIO()
        speech.write_to_fp(fp)
        fp.seek(0)
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        if savefile:
            speech.save(savefile)
        if block:
            while pygame.mixer.music.get_busy():
                sleep(0.1)


if __name__ == '__main__':
    Speaker.say('Welcome to the Code as Policies Demo!', block=True)

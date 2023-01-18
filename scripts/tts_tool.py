import playsound, winsound, pygame, time
from gtts import gTTS
from pathlib import Path


def tts(text):
    tts_t = gTTS(text)
    tts_t.save("sounds/audio.mp3")
    # pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/audio.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    pygame.mixer.music.unload()
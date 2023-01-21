import playsound, winsound, time, os
from gtts import gTTS
from pathlib import Path
from pydub import AudioSegment


def tts(text):
    tts_t = gTTS(text)
    tts_t.save("sounds/audio.mp3")
    sound = AudioSegment.from_mp3("sounds/audio.mp3")
    sound.export("sounds/audio.wav", format="wav")
    # pygame.init()
    winsound.PlaySound("sounds/audio.wav",winsound.SND_NODEFAULT |  winsound.SND_FILENAME)
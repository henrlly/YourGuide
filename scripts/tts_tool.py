import playsound
from gtts import gTTS
from pathlib import Path


def tts(text):
    tts_t = gTTS(text)
    tts_t.save("sounds/audio.mp3")
    audio = Path(__file__).parent.parent/'sounds'/"audio.mp3"
    playsound.playsound(audio)
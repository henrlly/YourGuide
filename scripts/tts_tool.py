import playsound
from gtts import gTTS
from pathlib import Path


def tts(text):
    tts_t = gTTS(text)
    tts_t.save('audio.mp3')
    audio = Path().cwd() / "audio.mp3"
    playsound.playsound(audio)
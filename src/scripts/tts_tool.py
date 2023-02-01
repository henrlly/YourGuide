import winsound
from gtts import gTTS
from pydub import AudioSegment

#proxy setting (if required)#
from misc.proxy_config import change_proxy
change_proxy('http://127.0.0.1:2802')

def tts(text):
    tts_t = gTTS(text)
    tts_t.save("sounds/audio.mp3")
    sound = AudioSegment.from_mp3("sounds/audio.mp3")
    sound.export("sounds/audio.wav", format="wav")
    winsound.PlaySound("sounds/audio.wav",winsound.SND_NODEFAULT |  winsound.SND_FILENAME)
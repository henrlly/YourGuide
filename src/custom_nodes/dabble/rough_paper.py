# import playsound
# audio = ''
# playsound.playsound()

import os, playsound
cwd = os.getcwd()
# print(os.path.dirname(__file__))
audio_file = 'beep-07a.mp3'
audio = os.path.join(cwd,f'sounds/{audio_file}')
playsound.playsound(audio)

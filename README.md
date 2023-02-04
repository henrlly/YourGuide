### Dependencies
playsound, gtts, pyaudio, peekingduck and SpeechRecognition, winsound, cuda 11.7, pytorch, ultralytics, pydub
install ffmpeg from https://github.com/BtbN/FFmpeg-Builds/releases/

NOTE: peekingduck is buggy with python 3.10 and above, use python<=3.9.13

get dependencies with
```
pip install -r requirements.txt --no-deps
```


### How to use
Download folder and run run.py

**-----------------------------------------------------------------------------------------------------------------------------------------------**
### NOTE: this program only supports the windows OS for now. However, this program is meant for mobile phones. 
To experience what it is like to use this program in mobile phones as intended, please follow the steps below.
1. Visit https://www.dev47apps.com
2. Download DroidCam on your mobile device (available on both IOS and Android). You DO NOT have to download DroidCam on your computer.
3. Make sure your computer and mobile device is connected to the SAME WiFi network.
4. Open DroidCam. It will show you your ***WiFi IP*** and your ***DroidCam Port*** (by default usually 4747).
5. In pipeline_config_format.yml, change input source to **http://<***WiFi IP***>:<***DroidCam Port***>/video** (E.G.http://196.168.200.200:4747/video)
6. **Done!** You can just fix your mobile device on your body and run run.py

**NOTE: please wait for the webcam connection to stablise after running run.py. It is usually very laggy at first but it will stablise in a moment(i.e. the peekingduck cv2 windows receives live video signal from your mobile device almost without any lag, provided that you have a decent network connection). The time taken for the connection to stablise is usally considerably shorter on IOS than that on Android.**

Alternatively if you want to just execute the program on your computer, change source number to 0(i.e. webcam) in pipeline_config_format.yml 

**------------------------------------------------------------------------------------------------------------------------------------------------**

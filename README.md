<img src="https://lh4.googleusercontent.com/V-6OoK7yo2J-VMXkTOWCntp8h_y8MXOdIhbgHS__bb21mAu7RO7ikYJLFB6eQU0j79M=w2400" data-canonical-src="https://lh4.googleusercontent.com/V-6OoK7yo2J-VMXkTOWCntp8h_y8MXOdIhbgHS__bb21mAu7RO7ikYJLFB6eQU0j79M=w2400"/>

**A tool to help the visually impaired or accurately locate and navigate towards items, and navigate surroundings.**

This project was made with [PeekingDuck](https://github.com/aisingapore/PeekingDuck) and achieved top 8 at the [National AI Student Challenge 2022](https://learn.aisingapore.org/national-ai-student-challenge-2022/)

# Features
 - Item Detection
 - Door Detection
 - Currency Detecion
 - 3D Surround Sound
 
# More info
[Youtube Video Link](https://youtu.be/dM9HiL169Ts)

[Project Proposal Docs](https://drive.google.com/file/d/1EVDFVZjpRslW4Aq669ZsxmdjW251BT0F/view?usp=sharing)

[Presentation Slides](https://docs.google.com/presentation/d/1ZWp2fdp2VQHpYRI-V2839Wg3ltqyxYBvUTPefOD4YRE/edit?usp=sharing)

# Models and datasets used
  - [YOLOv8](https://github.com/ultralytics/ultralytics)
  - [DoorDetect dataset](https://github.com/MiguelARD/DoorDetect-Dataset)

## Dependencies
Libraries used: playsound, gtts, pyaudio, peekingduck and SpeechRecognition, winsound, cuda 11.7, pytorch, ultralytics, pydub

Install ffmpeg from https://github.com/BtbN/FFmpeg-Builds/releases/

NOTE: peekingduck is buggy with python 3.10 and above, use python<=3.9.13

Get dependencies with
```
pip install -r requirements.txt --no-deps
```


## How to use
Download folder and run run.py

### NOTE: This program only supports the Windows OS for now. However, this program is meant for mobile phones. 
(Optional) To experience what it is like to use this program on mobile phones as intended, please follow the steps below.
1. Visit https://www.dev47apps.com
2. Download DroidCam on your mobile device (available on both IOS and Android). You DO NOT have to download DroidCam on your computer.
3. Make sure your computer and mobile device is connected to the SAME WiFi network.
4. Open DroidCam. It will show you your ***WiFi IP*** and your ***DroidCam Port*** (by default usually 4747).
5. In pipeline_config_format.yml AND pipeline_config_banknote.yml, change input source to **http://<***WiFi IP***>:<***DroidCam Port***>/video**  
(e.g. http://196.168.200.200:4747/video)
6. **Done!** You can just fix your mobile device on your body and run run.py

**NOTE: Please wait for the webcam connection to stablise after running run.py. It is usually very laggy at first but it will stablise in a moment (i.e. the peekingduck cv2 windows receives live video signal from your mobile device almost without any lag, provided that you have a decent network connection). The time taken for the connection to stablise is usally considerably shorter on IOS than that on Android.**

Alternatively if you want to just execute the program on your computer, change input source to 0 (i.e. webcam) in pipeline_config_format.yml and pipeline_config_banknote.yml and run run.py

import os, sys


from scripts.tts_tool import tts
import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def get_response_item():
    PROMPT_LIMIT = 5
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    for j in range(PROMPT_LIMIT):
        tts(f'Try {j+1}. Find an item. Speak!')

        guess = recognize_speech_from_mic(recognizer, microphone)
        if guess["transcription"]:
            break
        if not guess["success"]:
            break
        tts("I didn't catch that. What did you say?")

    if guess["error"]:
        tts("ERROR: {}".format(guess["error"]))
        exit()
    else:
        
        tts("You said: {}".format(guess["transcription"]))

    return guess["transcription"].lower()

def get_response_mode():
    PROMPT_LIMIT = 5
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    for j in range(PROMPT_LIMIT):
        tts(f'Try {j+1}. Choose mode: surround sound or frequency. Speak!')

        guess = recognize_speech_from_mic(recognizer, microphone)
        if guess["transcription"]:
            break
        if not guess["success"]:
            break
        tts("I didn't catch that. What did you say?")

    if guess["error"]:
        tts("ERROR: {}".format(guess["error"]))
        exit()
    else:
        
        tts("You said: {}".format(guess["transcription"]))

    return guess["transcription"].lower()

if __name__ == '__main__':

    item = get_response_item()
    mode = get_response_mode()

    
    ### Placeholder for the specified object and mode ###
    with open('specified_object.txt','w') as f:
        f.write(item)
    with open('sound_mode.txt','w') as f:
        f.write(mode)
    ### placeholder end ###

    with open('pipeline_config_format.yml', 'r') as f:
        pipeline_data = f.read()

    if item == 'door':
        pipeline_data = pipeline_data.replace('# - custom_nodes.model.model-door', '- custom_nodes.model.model-door')
    else:
        pipeline_data = pipeline_data.replace('# - custom_nodes.model.yolov8', '- custom_nodes.model.yolov8')

        with open('yolov8_config.yml', 'r') as f:
            f_data = f.read()
        n_data = f_data.replace('*', item)
        with open('src/custom_nodes/configs/model/yolov8.yml', 'w') as f:
            f.write(n_data)

    with open('pipeline_config.yml', 'w') as f:
        f.write(pipeline_data)

    os.system('cmd /c "peekingduck run"')
    
import os, sys


from scripts.tts_tool import tts
import speech_recognition as sr

#requires playsound, gtts, pyaudio and SpeechRecognition


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



if __name__ == '__main__':

    PROMPT_LIMIT = 5
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    for j in range(PROMPT_LIMIT):
        tts(f'Try {j+1}. Speak!')

        guess = recognize_speech_from_mic(recognizer, microphone)
        if guess["transcription"]:
            break
        if not guess["success"]:
            break
        tts("I didn't catch that. What did you say?")

    if guess["error"]:
        tts("ERROR: {}".format(guess["error"]))
        
    else:
        
        tts("You said: {}".format(guess["transcription"]))
        
        with open('pipeline_config.txt', 'r') as f:
            f_data = f.read()
        n_data = f_data.replace('*', guess["transcription"])

        ### Placeholder for the specified object ###
        with open('specified_object.txt','w') as f:
            f.write(guess["transcription"])
        ### edit end ###

        with open('pipeline_config.yml', 'w') as f:
            f.write(n_data)

        os.system('cmd /c "peekingduck run"')
    
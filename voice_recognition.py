import pyaudio
import json
import os
from typing import Callable
from vosk import KaldiRecognizer, Model
from keyword_recognition import has_keyword

# Constants for audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
FRAMES_PER_BUFFER = 8192
READ_BUFFER_SIZE = 4096

vosk_model_path = os.getenv(r'VOSK_MODEL_PATH')
model = Model(vosk_model_path)
recognizer = KaldiRecognizer(model, 16000)


def process_audio_stream(callback: Callable[[str], bool]) -> str:
    """
     Process audio input from the default microphone, uses a callback function
     to determine what to do with the transcribed text, and returns all
     transcribed text.

     Parameters:
     callback (function): A function to call with the transcribed text. It
                          should return True to continue processing, or False
                          to stop.

     Returns:
     str: All transcribed text concatenated together.
     """
    mic = pyaudio.PyAudio()
    stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                      input=True, frames_per_buffer=FRAMES_PER_BUFFER)
    stream.start_stream()

    formatted_text = None

    try:
        while True:
            data = stream.read(READ_BUFFER_SIZE)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                formatted_text = result.get('text', '')

                # Call the callback function with the transcribed text
                if not callback(formatted_text):
                    break
    finally:
        stream.close()
        mic.terminate()
        return formatted_text


def transcribe_audio_callback(text: str) -> bool:
    """
    Callback function for transcribing audio.
    Always returns False to stop after first transcription.

    Parameters:
    text (str): The transcribed text.

    Returns:
    bool: False, indicating to stop processing.
    """
    print(text)  # or handle the text as needed
    return False  # Stop after the first transcription


def listen_for_keywords_callback(text: str) -> bool:
    """
    Callback function for listening for keywords. Checks if a keyword is
    present and returns False if a keyword is detected to stop processing.

    Parameters:
    text (str): The transcribed text.

    Returns:
    bool: True to continue processing, False to stop if a keyword is detected.
    """
    if has_keyword(text):
        print(f"Keyword detected in text: {text}")
        return False  # Stop processing if a keyword is detected
    return True  # Continue processing


def transcribe_audio() -> str:
    """
    Transcribe audio input from the default microphone using Vosk local speech
    recognition.

    Returns:
        str: transcribed text.
    """
    return process_audio_stream(transcribe_audio_callback)


def listen_for_keywords() -> str:
    """
    Continuously listens until a keyword or set of keywords are spoken in a
    sentence.

    Returns
        str: the transcribed text up to the point a keyword was detected.
    """
    return process_audio_stream(listen_for_keywords_callback)

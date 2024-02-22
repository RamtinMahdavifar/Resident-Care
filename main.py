import os

import numpy as np
import pyaudio
import pygame
from TTS.api import TTS
from vosk import KaldiRecognizer, Model

from keyword_detector import check_for_keywords
from chatgpt_prompts import generate_response, summarize_conversation_history
from sms_twilio import send_mms

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC_ph")

model = Model(r"vosk-model-en-us-0.42-gigaspeech")
recognizer = KaldiRecognizer(model, 16000)

# Initialize the mixer module for audio playback
pygame.mixer.init()


def beep(frequency, duration):
    """
    Play a beep sound at a specified frequency and duration.

    Parameters:
    frequency (int): The frequency of the beep in Hertz.
    duration (int): The duration of the beep in milliseconds.
    """
    # Constants
    SAMPLE_RATE = 44100  # Sample rate in Hertz

    # Conversion factor from milliseconds to seconds
    MILLISECONDS_TO_SECONDS = 1000.0

    CHANNELS = 2  # Number of audio channels
    BITS_PER_SAMPLE = 16  # Number of bits per audio sample
    MAX_SAMPLE_VALUE = 2 ** (
                BITS_PER_SAMPLE - 1) - 1  # Maximum value for a sample

    # Generate a sound buffer with the given frequency
    n_samples = int(round(duration * SAMPLE_RATE / MILLISECONDS_TO_SECONDS))
    buf = np.zeros((n_samples, CHANNELS), dtype=np.int16)

    for s in range(n_samples):
        t = float(s) / SAMPLE_RATE  # time in seconds

        # Generate the sound for both left and right channels
        sample_value = int(
            round(MAX_SAMPLE_VALUE * np.sin(2 * np.pi * frequency * t)))
        buf[s][0] = sample_value  # left channel
        buf[s][1] = sample_value  # right channel

    sound = pygame.sndarray.make_sound(buf)

    # Play the sound
    sound.play(-1)
    pygame.time.delay(duration)
    sound.stop()


# Define the robot emoji for display purposes
AI_Response = "AI Response"


def transcribe_audio():
    """
    Transcribe audio input from the default microphone using Vosk local speech
    recognition.

    Returns:
    str: The transcribed text.
    """
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000,
                      input=True, frames_per_buffer=8192)

    stream.start_stream()

    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            formatted_text = text[14:-3]

            if len(formatted_text) == 0:
                continue

            else:

                stream.close()
                mic.terminate()
                return formatted_text


def remove_temp_files(file_path):
    """
    Remove temporary files created during the process.

    Parameters:
    file_path (str): The path to the file to remove.
    """
    os.remove(file_path)


def play_audio_pygame(file_path):
    """
     Plays an audio file

     Parameters:
     file_path (str): The path of the file to play.
     """
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Allow the audio to play for the duration of the file
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def process_and_play_response(response_text):
    """
    Process the response text, synthesize speech, save to a temporary file,
    and play the audio.

    Parameters:
    response_text (str): The text to synthesize and play as audio.
    """

    output_directory = "output"  # Change this to the desired directory name

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    output_file_path = os.path.join(output_directory, "output.wav")

    try:
        tts.tts_to_file(text=response_text, file_path=output_file_path)
        play_audio_pygame(output_file_path)

    finally:
        # Delete the file after playing
        remove_temp_files(output_file_path)


def recognize_keywords():
    """
     Continuously listens until a keyword or set of keywords are spoken in a
     sentence

     Returns:
     str: The sentence where a keyword was detected

     """
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000,
                      input=True, frames_per_buffer=8192)

    stream.start_stream()

    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            formatted_text = text[14:-3]

            if len(formatted_text) == 0:
                continue

            if check_for_keywords(formatted_text):
                stream.close()
                mic.terminate()
                return formatted_text


def main(stop_keyword="stop", exit_keyword="exit"):
    """
    Main function to run the Azure Speech Integration with ChatGpt Demo.

    Parameters:
    activation_keyword (str): The keyword to activate the conversation.
    stop_keyword (str): The keyword to stop and restart the conversation.
    exit_keyword (str): The keyword to exit the conversation.
    """

    while True:
        print("\nSystem Listening")

        input_text = recognize_keywords()
        print(f"\nYou: \n{input_text}\n")

        conversation_history = []

        response_text = generate_response(input_text, conversation_history, 1)

        # Process the response and play the response audio
        print(f"{AI_Response} Assistant:\n")
        process_and_play_response(response_text)

        running = True
        while running:

            beep(800, 200)  # Play a beep at 800 Hz for 200 milliseconds
            input_text = transcribe_audio()
            print(f"\nYou: {input_text}\n")

            # handle conversation aspect here
            response_text = generate_response(input_text,
                                              conversation_history, 1)

            print(f"{AI_Response} Assistant:\n")

            # Process the response and play the response audio
            process_and_play_response(response_text)

            response_text = "Do you require assistance?"
            print(f"{AI_Response} Assistant:\n")
            process_and_play_response(response_text)

            beep(800, 200)

            input_text = transcribe_audio()
            print(f"\nYou: {input_text}\n")

            if "yes" in input_text.lower():
                response_text = "Sending SMS, Assistance is on the way!"
                print(f"{AI_Response} Assistant:\n")
                process_and_play_response(response_text)

                # Summarising conversation and sending SMS to resident
                summarized_conversation = summarize_conversation_history(
                    conversation_history)

                print("Summarized Conversation sent to caregiver:\n" +
                      summarized_conversation + "\n")

                send_mms(summarized_conversation)
                conversation_history.clear()
                break

            else:
                response_text = generate_response(input_text,
                                                  conversation_history, 1)

                process_and_play_response(response_text)
                conversation_history.clear()
                break


if __name__ == "__main__":
    main(stop_keyword="stop", exit_keyword="exit")

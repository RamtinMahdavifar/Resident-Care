import os
import pygame
from TTS.api import TTS

from utilities import remove_temp_files

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC_ph")


def play_audio_file(file_path):
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
        play_audio_file(output_file_path)

    finally:
        # Delete the file after playing
        remove_temp_files(output_file_path)

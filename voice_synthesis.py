import os
import pygame
from TTS.api import TTS

from utilities import remove_temp_files

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC_ph")


def synthesize_speech(text, output_directory="output", filename="output.wav"):
    """
    Synthesize speech from text and save it to a file.

    Parameters:
    text (str): The text to synthesize.
    output_directory (str): The directory to save the synthesized audio file.
    filename (str): The name of the file to save the synthesized audio.

    Returns:
    str: The path to the synthesized audio file.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    output_file_path = os.path.join(output_directory, filename)

    # Use the TTS model to synthesize the text into an audio file
    tts.tts_to_file(text=text, file_path=output_file_path)

    return output_file_path


def play_audio_file(file_path):
    """
    Plays an audio file

    Parameters:
    file_path (str): The path of the file to play.
    """

    # Times per second to check if the audio is still playing
    check_audio_frequency = 10

    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Allow the audio to play for the duration of the file
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(check_audio_frequency)


def process_and_play_response(response_text):
    """
    Process the response text, synthesize speech, save to a temporary file,
    and play the audio.

    Parameters:
    response_text (str): The text to synthesize and play as audio.
    """
    output_file_path = None
    try:
        # Synthesize the speech and get the path to the audio file
        output_file_path = synthesize_speech(response_text)

        # Play the synthesized speech
        play_audio_file(output_file_path)

    finally:
        # Delete the file after playing
        remove_temp_files(output_file_path)
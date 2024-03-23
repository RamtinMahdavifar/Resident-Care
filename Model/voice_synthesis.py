import os
import pygame
from TTS.api import TTS

from Model.utilities import remove_temp_files, suppress_stdout

tts_model_name = os.getenv('TTS_MODEL_NAME')
tts = TTS(model_name=tts_model_name)



def synthesize_speech(text: str, output_directory: str = "output",
                      filename: str = "output.wav") -> str:
    """
    Synthesize speech from text and save it to a file.

    Parameters:
    text (str): The text to synthesize.
    output_directory (str): The directory to save the synthesized audio file.
    filename (str): The name of the file to save the synthesized audio.

    Returns:
    str: The path to the synthesized audio file.
    """

    with suppress_stdout():
        # Create the output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        output_file_path = os.path.join(output_directory, filename)

        # Use the TTS model to synthesize the text into an audio file
        tts.tts_to_file(text=text, file_path=output_file_path)

        return output_file_path


def play_audio_file(file_path: str) -> None:
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


def process_and_play_response(response_text: str) -> None:
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
        if output_file_path is not None:
            remove_temp_files(output_file_path)

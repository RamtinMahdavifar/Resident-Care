import os
import tempfile
import azure.cognitiveservices.speech as speechsdk
import openai
import config
import pygame
from IPython.display import Audio
import numpy as np

# Initialize the mixer module for audio playback
pygame.mixer.init()


def beep(frequency, duration):
    """
    Play a beep sound at a specified frequency and duration.

    Parameters:
    frequency (int): The frequency of the beep in Hertz.
    duration (int): The duration of the beep in milliseconds.
    """
    # Generate a sound buffer with the given frequency
    sample_rate = 44100
    n_samples = int(round(duration * sample_rate / 1000.0))
    buf = np.zeros((n_samples, 2), dtype=np.int16)
    max_sample = 2 ** (16 - 1) - 1
    for s in range(n_samples):
        t = float(s) / sample_rate  # time in seconds
        buf[s][0] = int(round(max_sample * np.sin(2 * np.pi * frequency * t)))  # left channel
        buf[s][1] = int(round(max_sample * np.sin(2 * np.pi * frequency * t)))  # right channel
    sound = pygame.sndarray.make_sound(buf)

    # Play the sound
    sound.play(-1)
    pygame.time.delay(duration)
    sound.stop()


# Define the robot emoji for display purposes
AI_Response = "AI Response"


def transcribe_audio(speech_config):
    """
    Transcribe audio input from the default microphone using Azure Speech Service.

    Parameters:
    speech_config (SpeechConfig): The configuration for speech service.

    Returns:
    str: The transcribed text.
    """
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once_async().get()
    return result.text.strip()


def generate_response(input_text, conversation_history):
    """
    Generate a response to the input text using OpenAI's GPT model.

    Parameters:
    input_text (str): The user's input text to respond to.
    conversation_history (list): The history of the conversation.

    Returns:
    str: The generated response text.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]

    messages.extend(conversation_history)
    messages.append({"role": "user", "content": input_text})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=1.3,
    )

    return response['choices'][0]['message']['content']


def synthesize_and_save_speech(speech_config, response_text, file_path):
    """
    Synthesize speech from text and save it to a file.

    Parameters:
    speech_config (SpeechConfig): The configuration for speech synthesis.
    response_text (str): The text to synthesize.
    file_path (str): The file path to save the synthesized audio.
    """
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = speech_synthesizer.speak_text_async(response_text).get()

    with open(file_path, "wb") as f:
        f.write(result.audio_data)


def play_audio(audio_file_path):
    """
    Play an audio file.

    Parameters:
    audio_file_path (str): The path to the audio file to play.
    """
    Audio(audio_file_path)


def remove_temp_files(file_path):
    """
    Remove temporary files created during the process.

    Parameters:
    file_path (str): The path to the file to remove.
    """
    os.remove(file_path)


def process_and_play_response(speech_config, response_text):
    """
    Process the response text, synthesize speech, save to a temporary file, and play the audio.

    Parameters:
    speech_config (SpeechConfig): The configuration for speech synthesis.
    response_text (str): The text to synthesize and play as audio.
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        audio_file_path = f.name

    try:
        synthesize_and_save_speech(speech_config, response_text, audio_file_path)
        play_audio(audio_file_path)
    finally:
        remove_temp_files(audio_file_path)


def main(stop_keyword="stop", exit_keyword="exit"):
    """
    Main function to run the Azure Speech Integration with ChatGpt Demo.

    Parameters:
    stop_keyword (str): The keyword to stop and restart the conversation.
    exit_keyword (str): The keyword to exit the conversation.
    """
    print("Azure Speech Integration with ChatGpt Demo")

    # Load assistance keywords from a file
    with open('assistance_keywords.txt', 'r') as file:
        assistance_keywords = [line.strip() for line in file.readlines()]

    # Define speech config
    azure_api_key = config.azure_api_key
    azure_region = config.azure_region
    voice = "en-US-ChristopherNeural"
    speech_config = speechsdk.SpeechConfig(subscription=azure_api_key, region=azure_region)
    speech_config.speech_synthesis_voice_name = voice
    openai.api_key = config.openai_api_key

    conversation_history = []

    running = True
    while running:
        print(AI_Response + " Listening...")
        beep(800, 200)  # Play a beep at 800 Hz for 200 milliseconds

        input_text = transcribe_audio(speech_config)
        print(f"You: {input_text}")

        # Check for assistance keywords
        if any(keyword.lower() in input_text.lower() for keyword in assistance_keywords):
            out = "Sending SMS, Assistance is on the way!"
            print(out)
            process_and_play_response(speech_config, out)

            # Here we would need to do further logic to figure out if they actually need help and hend an sms
            break

        if stop_keyword.lower() in input_text.lower():
            print("Restarting prompt...")
            conversation_history = []
            continue

        if exit_keyword.lower() in input_text.lower():
            out = "Goodbye for now..."
            print(out)
            process_and_play_response(speech_config, out)
            break

        response_text = generate_response(input_text, conversation_history)
        print(f"{AI_Response} Assistant: {response_text}")

        # Process the response and play the response audio
        process_and_play_response(speech_config, response_text)

        conversation_history.append({"role": "user", "content": input_text})
        conversation_history.append({"role": "assistant", "content": response_text})


if __name__ == "__main__":
    main(stop_keyword="stop", exit_keyword="exit")

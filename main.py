import os
import azure.cognitiveservices.speech as speechsdk
import openai
import pygame
import numpy as np
import pyaudio
from assistance_detector import check_for_assistance

from vosk import Model, KaldiRecognizer
from TTS.api import TTS

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC_ph")

model = Model(r"vosk-model-en-us-0.42-gigaspeech")
recognizer = KaldiRecognizer(model, 16000)

# Initialize the mixer module for audio playback
pygame.mixer.init()

print("System Listening")


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
        {"role": "system", "content": "You are a helpful assistant and need to figure out if a hospital or nursing \
        home resident requires assistance"},
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


def remove_temp_files(file_path):
    """
    Remove temporary files created during the process.

    Parameters:
    file_path (str): The path to the file to remove.
    """
    os.remove(file_path)


def play_audio_pygame(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Allow the audio to play for the duration of the file
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def process_and_play_response(response_text):
    """
    Process the response text, synthesize speech, save to a temporary file, and play the audio.

    Parameters:
    speech_config (SpeechConfig): The configuration for speech synthesis.
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
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            formatted_text = str(text[14:-3])

            if len(formatted_text) == 0:
                continue

            if check_for_assistance(formatted_text):
                stream.close()
                return formatted_text


def main(stop_keyword="stop", exit_keyword="exit"):
    """
    Main function to run the Azure Speech Integration with ChatGpt Demo.

    Parameters:
    activation_keyword (str): The keyword to activate the conversation.
    stop_keyword (str): The keyword to stop and restart the conversation.
    exit_keyword (str): The keyword to exit the conversation.
    """

    text = recognize_keywords()
    print(text)
    process_and_play_response(text)

    #
    # # Load assistance keywords from a file
    # with open('assistance_keywords.txt', 'r') as file:
    #     assistance_keywords = [line.strip() for line in file.readlines()]
    #
    # # Define speech config
    #
    # load_dotenv()
    # azure_api_key = os.getenv('AZURE_API_KEY')
    # azure_region = os.getenv('AZURE_REGION')
    # openai.api_key = os.getenv('OPENAI_API_KEY')
    # voice = "en-US-ChristopherNeural"
    # speech_config = speechsdk.SpeechConfig(subscription=azure_api_key, region=azure_region)
    # speech_config.speech_synthesis_voice_name = voice
    #
    # conversation_history = []
    #
    # running = True
    # while running:
    #     print(AI_Response + " Listening...")
    #
    #     beep(800, 200)  # Play a beep at 800 Hz for 200 milliseconds
    #     input_text = transcribe_audio(speech_config)
    #     print(f"You: {input_text}")
    #
    #     if any(keyword.lower() in input_text.lower() for keyword in assistance_keywords):
    #         response_text = "Do you require assistance?"
    #         print(f"{AI_Response} Assistant: {response_text}")
    #         process_and_play_response(speech_config, response_text)
    #
    #         beep(800, 200)  # Play a beep at 800 Hz for 200 milliseconds
    #
    #         input_text = transcribe_audio(speech_config)
    #         if len(input_text) == 0:
    #             continue
    #
    #         print(f"You: {input_text}")
    #
    #         if "yes" in input_text.lower():
    #             out = "Sending SMS, Assistance is on the way!"
    #             print(out)
    #             process_and_play_response(speech_config, out)
    #             # Here, integrate logic to send an SMS or provide assistance
    #             continue
    #
    #     if stop_keyword.lower() in input_text.lower():
    #         print("Restarting prompt...")
    #         conversation_history = []
    #         continue
    #
    #     if exit_keyword.lower() in input_text.lower():
    #         out = "Goodbye for now..."
    #         print(out)
    #         process_and_play_response(speech_config, out)
    #         break
    #
    #     # handle conversation aspect here
    #     response_text = generate_response(input_text, conversation_history)
    #     print(f"{AI_Response} Assistant: {response_text}")
    #
    #     # Process the response and play the response audio
    #     process_and_play_response(speech_config, response_text)
    #
    #     conversation_history.append({"role": "user", "content": input_text})
    #     conversation_history.append({"role": "assistant", "content": response_text})


if __name__ == "__main__":
    main(stop_keyword="stop", exit_keyword="exit")

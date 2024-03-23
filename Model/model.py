from Model.chatgpt_prompts import generate_response, \
    summarize_conversation_history, \
    is_urgent_assistance_needed, is_intent_to_end_conversation

from Model.sms_twilio import send_mms
from Model.voice_recognition import transcribe_audio, listen_for_keywords
from Model.utilities import beep
from Model.voice_synthesis import process_and_play_response


class CareBotModel:
    @staticmethod
    def generate_response(input_text, conversation_history):
        return generate_response(input_text, conversation_history)

    @staticmethod
    def summarize_conversation_history(conversation_history):
        return summarize_conversation_history(conversation_history)

    @staticmethod
    def is_urgent_assistance_needed(input_text):
        return is_urgent_assistance_needed(input_text)

    @staticmethod
    def is_intent_to_end_conversation(input_text):
        return is_intent_to_end_conversation(input_text)

    @staticmethod
    def send_mms(message):
        send_mms(message)

    @staticmethod
    def transcribe_audio():
        return transcribe_audio()

    @staticmethod
    def listen_for_keywords():
        return listen_for_keywords()

    @staticmethod
    def beep(frequency, duration):
        beep(frequency, duration)

    @staticmethod
    def process_and_play_response(message):
        process_and_play_response(message)

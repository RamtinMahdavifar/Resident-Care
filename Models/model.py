from Models.chatgpt_prompts import generate_response, \
    summarize_conversation_history, \
    is_urgent_assistance_needed, is_intent_to_end_conversation, \
    append_conversation_history

from Models.sms_twilio import send_mms
from Models.voice_recognition import transcribe_audio, listen_for_keywords
from Models.utilities import beep
from Models.voice_synthesis import process_and_play_response
from typing import List, Dict


class CareBotModel:
    @staticmethod
    def generate_response(
            input_text: str, conversation_history: List[Dict[str, str]]):
        return generate_response(input_text, conversation_history)

    @staticmethod
    def summarize_conversation_history(
            conversation_history: List[Dict[str, str]]):
        return summarize_conversation_history(conversation_history)

    @staticmethod
    def is_urgent_assistance_needed(input_text: str):
        return is_urgent_assistance_needed(input_text)

    @staticmethod
    def is_intent_to_end_conversation(input_text: str):
        return is_intent_to_end_conversation(input_text)

    @staticmethod
    def send_mms(message: str):
        send_mms(message)

    @staticmethod
    def transcribe_audio():
        return transcribe_audio()

    @staticmethod
    def listen_for_keywords():
        return listen_for_keywords()

    @staticmethod
    def beep(frequency: int, duration: int):
        beep(frequency, duration)

    @staticmethod
    def process_and_play_response(message: str):
        process_and_play_response(message)

    @staticmethod
    def append_conversation_history(
            input_text: str,
            response_text: str,
            conversation_history: List[Dict[str, str]]):
        append_conversation_history(input_text, response_text,
                                    conversation_history)

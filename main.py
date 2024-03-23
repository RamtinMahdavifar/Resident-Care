import textwrap
import os
import sys
import traceback

import streamlit as st
from typing import List, Dict

from Model.chatgpt_prompts import generate_response, \
    summarize_conversation_history, \
    is_urgent_assistance_needed, is_intent_to_end_conversation

from Model.sms_twilio import send_mms
from Model.voice_recognition import transcribe_audio, listen_for_keywords
from Model.utilities import beep
from Model.voice_synthesis import process_and_play_response

g_conversation_history: List[Dict[str, str]] = []
g_is_ui = False


def alert_assistance_request_sent() -> None:





def alert_ready() -> None:
    """
    Alerts the user that Care-Bot is ready and listening.
    """
    message_ready = "\nCare-Bot is ready and is listening.\n"
    print(message_ready)
    process_and_play_response(message_ready)
    beep(800, 200)


def handle_urgent_assistance(input_text: str) -> None:



def handle_conversation(input_text: str) -> None:


def say_goodbye() -> None:
    """
    Sends a goodbye message and clears the UI.
    """
    response_text = "Thank you. It seems you do not require further " \
                    "assistance. " \
                    "Feel free to chat with me anytime using my name " \
                    "Care-Bot. " \
                    "Goodbye for now.\n"
    display_streamlit_message(response_text, False)
    process_and_play_response(response_text)


def main() -> None:
    """
    Main function to run program.
    """
    initialize_ui()

    while True:
        g_conversation_history.clear()
        clear_streamlit_messages()

        alert_ready()
        input_text = listen_for_keywords()

        if is_urgent_assistance_needed(input_text):
            handle_urgent_assistance(input_text)
            continue

        handle_conversation(input_text)


if __name__ == "__main__":
    # Automatically detect if we are running as a streamlit application
    g_is_ui = is_streamlit()

    try:
        main()
    except Exception as e:
        # Capture and print the exception message to the console
        error_message = str(e)
        traceback_message = traceback.format_exc()  # This captures the full
        # traceback

        print("An error occurred:", error_message)
        print("Full traceback:", traceback_message)

        message = "Care-Bot is restarting due to a fatal error.\n"

        # Display the error message in the UI if running in Streamlit,
        # otherwise print to console
        if g_is_ui:
            display_streamlit_message(message, False)
            process_and_play_response(message)
            clear_streamlit()
        else:
            # Restart the script when not running in Streamlit UI mode
            print(message)
            os.execv(sys.executable, ['python'] + sys.argv)

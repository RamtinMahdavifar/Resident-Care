import textwrap
import os
import sys

from chatgpt_prompts import generate_response, \
    summarize_conversation_history, \
    is_urgent_assistance_needed, \
    is_assistance_needed_from_conversation_history, \
    is_intent_to_end_conversation, \
    append_conversation_history

from sms_twilio import send_mms
from voice_recognition import transcribe_audio, listen_for_keywords
from utilities import beep
from voice_synthesis import process_and_play_response
from typing import List

import streamlit as st

conversation_history: List[str] = []
is_ui = False

def alert_assistance_request_sent():
    response_text = "It seems you require assistance. Your request for " \
                    "assistance has been sent to your caregiver."
    print("CareBot AI Response:\n")

    display_message(response_text, False)
    process_and_play_response(response_text)

    # Summarising conversation and sending SMS to resident
    summarized_conversation = summarize_conversation_history(
        conversation_history)

    print("Summarized Conversation sent to caregiver:\n" +
          summarized_conversation + "\n")

    send_mms(summarized_conversation)
    conversation_history.clear()



# Function to render the sidebar with the logo
def render_sidebar(logo_url):
    st.sidebar.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="{logo_url}" style="width:250px;height:250px;"> </div> 
            <hr style='border: none; border-top: 1px solid #ccc; margin: 
            20px 0px;'> """,
        unsafe_allow_html=True,
    )


# Function to display a user or bot message in Streamlit
def display_message(message_text, is_user=True):
    if not is_ui:
        return

    color = "blue" if is_user else "#ADD8E6"
    text_color = "white" if is_user else "black"

    wrapped_text = textwrap.fill(message_text, width=70 if is_user else 90)
    indented_text = "\n".join(
        [f"<div style='text-align: left;'>{line}</div>" for line in
         wrapped_text.splitlines()]
    )

    st.markdown(
        f"<div style='padding: 10px;'>"
        f"<div style='background-color: {color}; padding: 10px; "
        f"border-radius: 5px; color: {text_color}; text-align: left;'>"
        f"{indented_text}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


def clear_streamlit():
    """
    Clears all messages, widgets, and session state in the Streamlit app,
    effectively resetting the app to a clean state.
    """
    if not is_ui:
        return

    # Clear session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    # Use Streamlit's rerun to refresh the app and clear the
    # screen
    st.rerun()


def main():
    """
    Main function to run program.
    """
    if is_ui:
        logo = "https://img.freepik.com/premium-vector/cute-nurse-holding" \
               "-health-symbol_123847-1477.jpg"
        render_sidebar(logo)
        st.title("🤖 Care-Bot Ai")
        st.markdown("<style>body {font-size: 18px;}</style>",
                    unsafe_allow_html=True)
        st.text("🤖  Listening...")

    while True:
        conversation_history.clear()
        message_ready = "\nCare-Bot is ready and is listening.\n"

        print(message_ready)
        process_and_play_response(message_ready)

        beep(800, 200)

        input_text = listen_for_keywords()

        if is_urgent_assistance_needed(input_text):
            print(f"\nYou: \n{input_text}\n")
            display_message(input_text)

            append_conversation_history(input_text, "", conversation_history)
            alert_assistance_request_sent()
            clear_streamlit()
            continue

        while True:
            print(f"\nYou: \n{input_text}\n")
            display_message(input_text)

            response_text = generate_response(input_text, conversation_history)
            print(" CareBot AI Response:\n")

            display_message(response_text, False)
            process_and_play_response(response_text)

            beep(800, 200)  # Play a beep at 800 Hz for 200 milliseconds
            input_text = transcribe_audio()

            if (is_assistance_needed_from_conversation_history(
                    input_text,
                    conversation_history)):
                print(f"\nYou: {input_text}\n")
                display_message(input_text)

                alert_assistance_request_sent()
                clear_streamlit()
                break

            elif is_intent_to_end_conversation(input_text):
                print(f"\nYou: {input_text}\n")
                response_text = "Thank you. It seems you do not require " \
                                "further " \
                                "assistance." \
                                "Feel free to chat with me anytime using my " \
                                "name " \
                                "Care-Bot. " \
                                "Goodbye for now.\n"
                display_message(response_text, False)
                process_and_play_response(response_text)
                clear_streamlit()
                break


if __name__ == "__main__":

    # automatically detect if we are running as a streamlit application
    is_ui = 'streamlit' in sys.modules

    # on any exception restart the System
    try:
        main()
    except:
        message = "Care-Bot is restarting do to a fatal " \
                  "error.\n"
        print(message)
        if is_ui:
            display_message(message, False)

        process_and_play_response(message)
        if is_ui:
            clear_streamlit()
        else:
            os.execv(sys.executable, ['python'] + sys.argv)

import textwrap
import os
import sys
import traceback

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
    """
    Alerts that an assistance request has been sent to the caregiver.

    This function performs several actions: - Notifies the user through both
    a visual message in the Streamlit app and audio feedback that their
    request for assistance has been communicated to their caregiver. -
    Summarizes the conversation history and sends it to the caregiver via
    SMS. - Clears the current conversation history after sending.
    """

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
def render_sidebar(logo_path):
    """
    Renders the sidebar in the Streamlit app with a logo from a local path
    and extended introductory text.

    Parameters: - logo_path (str): The local file path to the logo image to
    be displayed in the sidebar.

    The sidebar includes: - A logo centered at the top. - Detailed
    introductory text about the capabilities of Care-Bot, including
    listening for keywords and providing assistance.
    """

    # Display the image from a local path
    st.sidebar.image(logo_path, width=250,
                     caption="Care-Bot, your personal assistant 🤖")

    # Add the updated introductory text
    st.sidebar.markdown(
        """
        <hr style='border: none; border-top: 1px solid #ccc; margin:
         20px 0px;'>
        <p style='text-align: center; font-size: 16px;'>
            Hi there! I'm <strong>Care-Bot</strong>, your personal assistant
             🤖.
        </p>
        <p style='text-align: center; font-size: 16px;'>
            I'm here to help you by listening for keywords and situations where
             you may require assistance.
        </p>
        <p style='text-align: center; font-size: 16px;'>
            You can talk to me at any time using my name
             <strong>Care-Bot</strong>.
        </p>
        <p style='text-align: center; font-size: 16px;'>
            I'm always listening and ready to assist you with your needs.
        </p>
        """,
        unsafe_allow_html=True,
    )


def display_message(message_text, is_user=True):
    """
    Displays a message in the Streamlit app, with styling based on the
    message sender.

    Parameters: - message_text (str): The text of the message to be
    displayed. - is_user (bool, optional): Flag indicating whether the
    message is from the user (True) or the bot (False). Defaults to True.

    The function styles the message differently based on the sender: -
    User messages are displayed with a blue background and white text. -
    Bot messages are displayed with a light blue background and black text.

    Messages are wrapped to ensure a consistent and readable format,
    and each message is stored as a placeholder in the Streamlit session
    state for potential later removal.
    """
    if not is_ui:
        return

    color = "blue" if is_user else "#ADD8E6"
    text_color = "white" if is_user else "black"

    wrapped_text = textwrap.fill(message_text, width=70 if is_user else 90)
    message_html = "\n".join(
        [f"<div style='text-align: left;'>{line}</div>" for line in
         wrapped_text.splitlines()])

    message_display = st.markdown(
        f"<div style='padding: 10px;'>"
        f"<div style='background-color: {color}; padding: 10px; "
        f"border-radius: 5px; color: {text_color}; text-align: left;'>"
        f"{message_html}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Store the placeholder in the session state for later removal
    st.session_state['message_placeholders'].append(message_display)


def clear_streamlit():
    """
    Use Streamlit's rerun to refresh the app.
    """
    if not is_ui:
        return

    st.rerun()


def clear_messages():
    """
    Clears all messages displayed by the display_message function.
    """
    if not is_ui:
        return

    while st.session_state['message_placeholders']:
        message_placeholder = st.session_state['message_placeholders'].pop()
        message_placeholder.empty()  # Clear the placeholder


def main():
    """
    Main function to run program.
    """
    if is_ui:
        logo = "Images/logo.jpg"
        render_sidebar(logo)
        st.title("🤖 Care-Bot Ai")
        st.markdown("<style>body {font-size: 18px;}</style>",
                    unsafe_allow_html=True)
        st.text("🤖  Listening...")

        # Function to display a user or bot message in Streamlit Initialize
        # a list in the session state to hold message placeholders if it
        # doesn't exist
        if 'message_placeholders' not in st.session_state:
            st.session_state['message_placeholders'] = []

    while True:
        conversation_history.clear()
        clear_messages()

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
            clear_messages()
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
                clear_messages()
                break

            elif is_intent_to_end_conversation(input_text):
                print(f"\nYou: {input_text}\n")
                display_message(input_text)
                response_text = "Thank you. It seems you do not require " \
                                "further " \
                                "assistance." \
                                "Feel free to chat with me anytime using my " \
                                "name " \
                                "Care-Bot. " \
                                "Goodbye for now.\n"
                display_message(response_text, False)
                process_and_play_response(response_text)
                clear_messages()
                break


def check_streamlit():
    """
    Function to check whether python code is run within streamlit

    Returns
    -------
    use_streamlit : boolean
        True if code is run within streamlit, else False
    """
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if not get_script_run_ctx():
            use_streamlit = False
        else:
            use_streamlit = True
    except ModuleNotFoundError:
        use_streamlit = False
    return use_streamlit


if __name__ == "__main__":
    # Automatically detect if we are running as a streamlit application
    is_ui = check_streamlit()

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
        if is_ui:
            display_message(message, False)
            process_and_play_response(message)
            clear_streamlit()
        else:
            # Restart the script when not running in Streamlit UI mode
            print(message)
            os.execv(sys.executable, ['python'] + sys.argv)

import textwrap

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
from streamlit_chat import message

conversation_history: List[str] = []



# Provide the path to your logo image file
logo = "https://img.freepik.com/premium-vector/cute-nurse-holding-health-symbol_123847-1477.jpg"



st.sidebar.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <img src="{}" style="width:250px;height:250px;">
    </div>
    <hr style='border: none; border-top: 1px solid #ccc; margin: 20px 0px;'>
    """.format(logo),
    unsafe_allow_html=True,
)

# Define the robot emoji
robot_emoji = "�"


def alert_assistance_request_sent():
    response_text = "It seems you require assistance. Your request for " \
                    "assistance has been sent to your caregiver."
    print("CareBot AI Response:\n")
    wrapped_response = textwrap.fill(response_text, width=70)
    indented_response = "\n".join(
        ["<div style='text-align: left;'>" + line + "</div>" for line in
         wrapped_response.splitlines()])

    st.markdown(
        f"<div style='background-color: #ADD8E6; padding: 10px; border-radius: 5px; text-align: left; color: black;'>"
        f"{indented_response}</div>",
        unsafe_allow_html=True)
    process_and_play_response(response_text)

    # Summarising conversation and sending SMS to resident
    summarized_conversation = summarize_conversation_history(
        conversation_history)

    print("Summarized Conversation sent to caregiver:\n" +
          summarized_conversation + "\n")

    send_mms(summarized_conversation)
    conversation_history.clear()


def main(is_ui = False):
    """
    Main function to run program.
    """

    if(is_ui):
        st.title("🤖 Care-Bot Ai")
        st.markdown("<style>body {font-size: 18px;}</style>",
                    unsafe_allow_html=True)

    while True:
        conversation_history.clear()
        print("\nSystem Listening")

        st.text(robot_emoji + " Listening...")
        input_text = listen_for_keywords()
        wrapped_input = textwrap.fill(input_text, width=90)
        indented_input = "\n".join(
            ["<div style='text-align: left;'>" + line + "</div>" for line in
             wrapped_input.splitlines()])

        st.markdown(f"<div style='padding: 30px;'>"
                    f"<div style='background-color: blue; padding: 10px; border-radius: 5px; color: white; text-align: left;'>"
                    f"{indented_input}</div>"
                    f"</div>",
                    unsafe_allow_html=True)

        if is_urgent_assistance_needed(input_text):
            print(f"\nYou: \n{input_text}\n")
            append_conversation_history(input_text, "", conversation_history)
            alert_assistance_request_sent()
            continue

        while True:
            print(f"\nYou: \n{input_text}\n")
            wrapped_input = textwrap.fill(input_text, width=90)
            indented_input = "\n".join(
                ["<div style='text-align: left;'>" + line + "</div>" for line
                 in
                 wrapped_input.splitlines()])

            st.markdown(f"<div style='padding: 30px;'>"
                        f"<div style='background-color: blue; padding: 10px; border-radius: 5px; color: white; text-align: left;'>"
                        f"{indented_input}</div>"
                        f"</div>",
                        unsafe_allow_html=True)

            response_text = generate_response(input_text, conversation_history)
            print(" CareBot AI Response:\n")

            wrapped_response = textwrap.fill(response_text, width=70)
            indented_response = "\n".join(
                ["<div style='text-align: left;'>" + line + "</div>" for line
                 in wrapped_response.splitlines()])

            st.markdown(
                f"<div style='background-color: #ADD8E6; padding: 10px; border-radius: 5px; text-align: left; color: black;'>"
                f"{indented_response}</div>",
                unsafe_allow_html=True)
            process_and_play_response(response_text)


            beep(800, 200)  # Play a beep at 800 Hz for 200 milliseconds
            input_text = transcribe_audio()

            if (is_assistance_needed_from_conversation_history(
                    input_text,
                    conversation_history)):
                print(f"\nYou: {input_text}\n")
                wrapped_input = textwrap.fill(input_text, width=90)
                indented_input = "\n".join(
                    ["<div style='text-align: left;'>" + line + "</div>" for
                     line in
                     wrapped_input.splitlines()])

                st.markdown(f"<div style='padding: 30px;'>"
                            f"<div style='background-color: blue; padding: 10px; border-radius: 5px; color: white; text-align: left;'>"
                            f"{indented_input}</div>"
                            f"</div>",
                            unsafe_allow_html=True)
                alert_assistance_request_sent()
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
                process_and_play_response(response_text)
                break


if __name__ == "__main__":
    main(is_ui=True)

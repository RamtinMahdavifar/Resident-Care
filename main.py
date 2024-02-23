from chatgpt_prompts import generate_response, summarize_conversation_history, \
    is_urgent_assistance_needed, \
    is_assistance_needed_from_conversation_history, \
    is_intent_to_end_conversation, \
    append_conversation_history

from sms_twilio import send_mms
from voice_recognition import transcribe_audio, listen_for_keywords
from utilities import beep
from voice_synthesis import process_and_play_response

conversation_history = []


def alert_assistance_request_sent():
    response_text = "It seems you require assistance. Your request for " \
                    "assistance has been sent to your caregiver."
    print("CareBot AI Response:\n")
    process_and_play_response(response_text)

    # Summarising conversation and sending SMS to resident
    summarized_conversation = summarize_conversation_history(
        conversation_history)

    print("Summarized Conversation sent to caregiver:\n" +
          summarized_conversation + "\n")

    send_mms(summarized_conversation)
    conversation_history.clear()


def main():
    """
    Main function to run program.
    """

    while True:
        conversation_history.clear()
        print("\nSystem Listening")

        input_text = listen_for_keywords()
        if is_urgent_assistance_needed(input_text):
            print(f"\nYou: \n{input_text}\n")
            append_conversation_history(input_text, "", conversation_history)
            alert_assistance_request_sent()
            continue

        while True:
            print(f"\nYou: \n{input_text}\n")

            response_text = generate_response(input_text, conversation_history)
            print(" CareBot AI Response:\n")
            process_and_play_response(response_text)

            beep(800, 200)  # Play a beep at 800 Hz for 200 milliseconds
            input_text = transcribe_audio()

            if (is_assistance_needed_from_conversation_history(
                    input_text,
                    conversation_history)):
                print(f"\nYou: {input_text}\n")
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
    main()

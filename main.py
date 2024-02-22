from chatgpt_prompts import generate_response, summarize_conversation_history
from sms_twilio import send_mms
from voice_recognition import transcribe_audio, listen_for_keywords
from utilities import beep
from voice_synthesis import process_and_play_response


def main():
    """
    Main function to run program.
    """

    ai_response = "AI Response"

    while True:
        print("\nSystem Listening")

        input_text = listen_for_keywords()
        print(f"\nYou: \n{input_text}\n")

        conversation_history = []

        response_text = generate_response(input_text, conversation_history, 1)

        # Process the response and play the response audio
        print(f"{ai_response} Assistant:\n")
        process_and_play_response(response_text)

        running = True
        while running:

            beep(800, 200)  # Play a beep at 800 Hz for 200 milliseconds
            input_text = transcribe_audio()
            print(f"\nYou: {input_text}\n")

            # handle conversation aspect here
            response_text = generate_response(input_text,
                                              conversation_history, 1)

            print(f"{ai_response} Assistant:\n")

            # Process the response and play the response audio
            process_and_play_response(response_text)

            response_text = "Do you require assistance?"
            print(f"{ai_response} Assistant:\n")
            process_and_play_response(response_text)

            beep(800, 200)

            input_text = transcribe_audio()
            print(f"\nYou: {input_text}\n")

            if "yes" in input_text.lower():
                response_text = "Sending SMS, Assistance is on the way!"
                print(f"{ai_response} Assistant:\n")
                process_and_play_response(response_text)

                # Summarising conversation and sending SMS to resident
                summarized_conversation = summarize_conversation_history(
                    conversation_history)

                print("Summarized Conversation sent to caregiver:\n" +
                      summarized_conversation + "\n")

                send_mms(summarized_conversation)
                conversation_history.clear()
                break

            else:
                response_text = generate_response(input_text,
                                                  conversation_history, 1)

                process_and_play_response(response_text)
                conversation_history.clear()
                break


if __name__ == "__main__":
    main()

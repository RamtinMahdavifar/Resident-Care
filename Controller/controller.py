from typing import List, Dict


class CareBotController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.conversation_history: List[Dict[str, str]] = []

    def alert_assistance_request_sent(self):
        """
        Alerts that an assistance request has been sent to the caregiver.

        This function performs several actions: - Notifies the user through
        both a visual message in the Streamlit app and audio feedback that
        their request for assistance has been communicated to their caregiver.

        Summarizes the conversation history and sends it to the caregiver via
        SMS. - Clears the current conversation history after sending.
        """

        response_text = "It seems you require assistance. Your request for " \
                        "assistance has been sent to your caregiver."
        print("CareBot AI Response:\n")

        self.view.display_streamlit_message(response_text, False)
        self.model.process_and_play_response(response_text)

        # Summarising conversation and sending SMS to resident
        summarized_conversation = self.model.summarize_conversation_history(
            self.conversation_history)

        print("Summarized Conversation sent to caregiver:\n"
              + summarized_conversation + "\n")

        self.model.send_mms(summarized_conversation)

    def handle_urgent_assistance(self, input_text):
        """
          Handles the scenario when urgent assistance is needed.
          """
        print(f"\nYou: \n{input_text}\n")
        self.view.display_streamlit_message(input_text)
        self.alert_assistance_request_sent()

    def handle_conversation(self, input_text):
        """
           Manages the conversation flow, including generating responses and
           checking for assistance needs or intent to end the conversation.
           """
        while True:
            print(f"\nYou: \n{input_text}\n")
            self.view.display_streamlit_message(input_text)

            response_text = self.model.generate_response(
                input_text, self.conversation_history)

            print("CareBot AI Response:\n")
            self.view.display_streamlit_message(response_text, False)
            self.model.process_and_play_response(response_text)

            self.model.beep(800, 200)
            input_text = self.model.transcribe_audio()

            if self.model.is_intent_to_end_conversation(input_text):
                self.say_goodbye()
                break

            elif self.model.is_urgent_assistance_needed(input_text):
                self.alert_assistance_request_sent()
                break

    def say_goodbye(self) -> None:
        """
        Sends a goodbye message and clears the UI.
        """
        response_text = "Thank you. It seems you do not require further " \
                        "assistance. " \
                        "Feel free to chat with me anytime using my name " \
                        "Care-Bot. " \
                        "Goodbye for now.\n"
        self.view.display_streamlit_message(response_text, False)
        self.model.process_and_play_response(response_text)

    def alert_ready(self) -> None:
        """
        Alerts the user that Care-Bot is ready and listening.
        """
        message_ready = "\nCare-Bot is ready and is listening.\n"
        print(message_ready)
        self.model.process_and_play_response(message_ready)
        self.model.beep(800, 200)

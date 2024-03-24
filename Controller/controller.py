import os
import sys
from typing import List, Dict


class CareBotController:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__conversation_history: List[Dict[str, str]] = []

    def get_model(self):
        return self.__model

    def get_view(self):
        return self.__view

    def get_conversation_history(self):
        return self.__conversation_history

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

        self.display_message(response_text, False)
        self.get_model().process_and_play_response(response_text)

        # Summarising conversation and sending SMS to resident
        summarized_conversation = self.get_model(
        ).summarize_conversation_history(
            self.get_conversation_history())

        summary = "Summarized Conversation sent to caregiver:\n" + \
                  summarized_conversation + "\n"

        self.display_message(summary, False)
        self.get_model().send_mms(summarized_conversation)

    def handle_urgent_assistance(self, input_text):
        """
        Handles the scenario when urgent assistance is needed.
        Returns true if urgent assistance case was handled.
        """
        if self.get_model().is_urgent_assistance_needed(input_text):
            self.display_message(input_text)
            self.alert_assistance_request_sent()
            return True
        else:
            return False

    def handle_conversation(self, input_text):
        """
        Manages the conversation flow, including generating responses and
        checking for assistance needs or intent to end the conversation.
        """
        NO_REPLY_THRESH_HOLD = 2
        no_replies_count = 0

        while True:
            self.display_message(input_text)

            response_text = self.get_model().generate_response(
                input_text, self.get_conversation_history())

            self.display_message(response_text, False)
            self.get_model().process_and_play_response(response_text)

            self.get_model().beep(800, 200)
            input_text = self.get_model().transcribe_audio()

            if len(input_text) == 0 or input_text is None:
                no_replies_count += 1

            if no_replies_count >= NO_REPLY_THRESH_HOLD:
                self.say_goodbye()
                break

            if self.get_model().is_intent_to_end_conversation(
                    input_text) or \
                    self.get_model().is_urgent_assistance_needed(
                        input_text):

                self.display_message(input_text)

                if self.get_model().is_intent_to_end_conversation(input_text):
                    self.say_goodbye()
                else:
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

        self.display_message(response_text, False)
        self.get_model().process_and_play_response(response_text)

    def alert_ready(self) -> None:
        """
        Alerts the user that Care-Bot is ready and listening.
        """
        message_ready = "\nCare-Bot is ready and is listening.\n"
        self.display_message(message_ready, False)

        self.get_model().process_and_play_response(message_ready)
        self.get_model().beep(800, 200)

    def listen_for_keywords(self):
        self.clear_conversation_history()
        self.alert_ready()
        return self.get_model().listen_for_keywords()

    def clear_conversation_history(self):
        self.get_conversation_history().clear()
        self.get_view().clear_streamlit_messages()

    def restart_system(self, error_message, traceback_message):
        print("An error occurred:", error_message)
        print("Full traceback:", traceback_message)

        message = "Care-Bot is restarting due to a fatal error.\n"
        self.display_message(message, False)
        self.get_model().process_and_play_response(message)

        if self.get_view().is_ui:
            # restart streamlit
            self.get_view().clear_streamlit()
        else:
            # Restart the script when not running in Streamlit UI mode
            print(message)
            os.execv(sys.executable, ['python'] + sys.argv)

    def display_message(self, message_text: str,
                        is_user: bool = True):
        if is_user:
            print(f"\nYou:\n{message_text}\n")

        else:
            print(f"\nCareBot AI Response:\n{message_text}\n")

        self.get_view().display_streamlit_message(message_text, is_user)

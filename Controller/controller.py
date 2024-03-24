import os
import sys
from typing import List, Dict

from Model.model import CareBotModel
from View.view import CareBotView


class CareBotController:
    def __init__(self, model: CareBotModel, view: CareBotView):
        self.__model = model
        self.__view = view
        self.__conversation_history: List[Dict[str, str]] = []

    def get_model(self) -> CareBotModel:
        """
        Returns the model component of the CareBot.

        Returns:
            object: The model component.
        """
        return self.__model

    def get_view(self) -> CareBotView:
        """
        Returns the view component of the CareBot.

        Returns:
            object: The view component.
        """
        return self.__view

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Returns the conversation history of the CareBot.

        Returns:
            List[Dict[str, str]]: The conversation history as a list of
            dictionaries, where each dictionary represents a conversation
            entry.
        """
        return self.__conversation_history

    def alert_assistance_request_sent(self):
        """
        Alerts that an assistance request has been sent to the caregiver.

        This function performs several actions:
        - Notifies the user through both a visual message in the Streamlit
          app and audio feedback that their request for assistance has been
          communicated to their caregiver.

        - Summarizes the conversation history and sends it to the caregiver via
          MMS
        """
        response_text = "It seems you require assistance. Your request for " \
                        "assistance has been sent to your caregiver."

        self.display_message(response_text, False)
        self.get_model().process_and_play_response(response_text)

        # Summarising conversation and sending MMS to resident
        summarized_conversation = self.get_model(
        ).summarize_conversation_history(
            self.get_conversation_history())

        summary = "Summarized Conversation sent to caregiver:\n" + \
                  summarized_conversation + "\n"

        self.display_message(summary, False)
        self.get_model().send_mms(summarized_conversation)

    def handle_urgent_assistance(self, input_text: str):
        """
        Handles the scenario when urgent assistance is needed.
        Returns:
             true if urgent assistance case was handled.
        """
        if self.get_model().is_urgent_assistance_needed(input_text):
            self.display_message(input_text)
            self.alert_assistance_request_sent()
            return True
        else:
            return False

    def handle_conversation(self, input_text: str):
        """
        Manages the conversation flow, including generating responses and
        checking for assistance needs or intent to end the conversation.

        Logic:
            - Initialize a threshold for no replies and a count for
              consecutive no replies.
            - Loop infinitely to manage the conversation flow.
                - Display the user's input.
                - Generate a response based on the input and the conversation
                  history.
                - Display the generated response.
                - Process and play the generated response.
                - Transcribe audio to get the next input text.
                - If the input text is empty or None, increase the count of no
                  replies.
                - If the count of no replies exceeds the threshold, say goodbye
                  and exit the loop.
                - If the input text indicates the intent to end the
                  conversation or urgent assistance is needed:
                    - Display the input text.
                    - If the intent is to end the conversation, say goodbye.
                    - If urgent assistance is needed, send an alert and exit
                      the loop.
        """
        NO_REPLY_THRESH_HOLD: int = 2
        no_replies_count: int = 0

        while True:
            self.display_message(input_text)

            response_text = self.get_model().generate_response(
                input_text, self.get_conversation_history())

            self.display_message(response_text, False)
            self.get_model().process_and_play_response(response_text)

            input_text = self.get_voice_input()

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
        Displays and plays a goodbye message.
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

    def clear_conversation_history(self):
        """
        Clears the conversation history and streamlit messages.

        This method clears the conversation history maintained by the
        CareBotController and also clears the messages displayed in the
        Streamlit UI, if applicable.
        """
        self.get_conversation_history().clear()
        self.get_view().clear_streamlit_messages()

    def restart_system(self, error_message: str, traceback_message: str):
        """
        Restarts the system after a fatal error.

        Args:
            error_message (str): The error message indicating the reason for
            the fatal error.
            traceback_message (str): The traceback message providing additional
            details about the error.

        This method prints the error message and traceback message, displays
        a message indicating
        that the Care-Bot is restarting due to a fatal error, and then
        restarts the system.

        If the system is running in Streamlit UI mode, it restarts
        Streamlit; otherwise, it restarts the script using the same command
        that launched it.
        """
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
        """
        Displays a message.

        Args:
           message_text (str): The text of the message to be displayed.
           is_user (bool, optional): A flag indicating whether the message is
           from the user (True) or the AI (False). Defaults to True.

        This method displays the specified message. If the message is from
        the user, it is preceded by "You:";

        if it is from the AI, it is preceded by "CareBot AI Response:".

        Additionally, if the system is running in Streamlit UI mode, the
        message is displayed in the UI.
               """
        if is_user:
            print(f"\nYou:\n{message_text}\n")

        else:
            print(f"\nCareBot AI Response:\n{message_text}\n")

        self.get_view().display_streamlit_message(message_text, is_user)

    def get_voice_input(self, is_listen_keywords: bool = False):
        """
        Gets voice input from the user.

        Args:
            is_listen_keywords (bool, optional): A flag indicating whether the
            system should listen for keywords. Defaults to False.

        Returns:
            str: The voice input from the user.

        This method beeps to indicate that it is ready to receive input and
        then either transcribes audio or listens for keywords based on the
        value of the is_listen_keywords flag.

        It clears the conversation history and alerts the system if keywords
        are being listened for.
        """
        self.get_model().beep(800, 200)
        if is_listen_keywords:
            self.clear_conversation_history()
            self.alert_ready()
            return self.get_model().listen_for_keywords()
        else:
            return self.get_model().transcribe_audio()

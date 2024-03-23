import textwrap
import os
import sys
import traceback

from Model.model import CareBotModel

from View.view import CareBotView
from Controller.controller import CareBotController

def main() -> None:
    """
    Main function to run program.
    """
    model = CareBotModel()
    view = CareBotView()
    controller = CareBotController(model, view)

    while True:
        controller.conversation_history.clear()

        controller.view.clear_streamlit_messages()

        controller.alert_ready()
        input_text = controller.model.listen_for_keywords()

        if controller.model.is_urgent_assistance_needed(input_text):
            controller.handle_urgent_assistance(input_text)
            continue

        controller.handle_conversation(input_text)


if __name__ == "__main__":
    # # Automatically detect if we are running as a streamlit application
    # g_is_ui = is_streamlit()
    main()
    # try:
    #     main()
    # except Exception as e:
        # # Capture and print the exception message to the console
        # error_message = str(e)
        # traceback_message = traceback.format_exc()  # This captures the full
        # # traceback
        #
        # print("An error occurred:", error_message)
        # print("Full traceback:", traceback_message)
        #
        # message = "Care-Bot is restarting due to a fatal error.\n"
        #
        # # Display the error message in the UI if running in Streamlit,
        # # otherwise print to console
        # if g_is_ui:
        #     display_streamlit_message(message, False)
        #     process_and_play_response(message)
        #     clear_streamlit()
        # else:
        #     # Restart the script when not running in Streamlit UI mode
        #     print(message)
        #     os.execv(sys.executable, ['python'] + sys.argv)

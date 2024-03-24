import traceback

from Models.CareBotModel import CareBotModel
from View.view import CareBotView
from Controller.controller import CareBotController


def main() -> None:
    """
    Main function to run program.
    """
    model: CareBotModel = CareBotModel()
    view: CareBotView = CareBotView()
    controller: CareBotController = CareBotController(model, view)

    try:
        while True:
            input_text: str = controller.get_voice_input(
                is_listen_keywords=True)

            if controller.handle_urgent_assistance(input_text):
                continue

            else:
                controller.handle_conversation(input_text)

    except Exception as e:
        error_message = str(e)
        traceback_message = traceback.format_exc()
        controller.restart_system(error_message, traceback_message)


if __name__ == "__main__":
    main()

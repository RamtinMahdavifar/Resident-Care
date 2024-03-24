import openai
import pytest

from Models.chatgpt_prompts import generate_response
from Models.sms_twilio import send_mms


@pytest.mark.smoke
def test_openai_version():
    """
     Tests if the OpenAI library version used matches the expected version.

     This test ensures that the version of the OpenAI library being used is
     exactly "0.28.0". It is crucial for maintaining compatibility and
     ensuring that any changes or deprecations introduced in newer versions
     do not affect the current implementation.
    """
    assert openai.__version__ == "0.28.0"


def test_gpt_response():
    """
    Tests the GPT Models's response generation to ensure it is not empty.

    This test calls the generate_response function with a sample input ("Hi
    ChatGPT") and checks that the response generated is not empty. It
    verifies that the GPT Models is correctly set up and capable of producing
    responses, ensuring the chat functionality is operational.
    """
    assert len(generate_response("Hi ChatGPT", [])) != 0


def test_send_mms():
    """
    Tests the functionality of sending an MMS to ensure it executes
    successfully.

    This test calls the send_mms function with a test message and asserts
    that the function returns True, indicating a successful execution. It is
    critical for verifying the operational status of the MMS sending
    feature, which involved Twilio. This test
    helps to ensure that the integration with Twilio is correctly
    configured and functional.
    """
    assert send_mms("This is a test MMS from the CI") is True

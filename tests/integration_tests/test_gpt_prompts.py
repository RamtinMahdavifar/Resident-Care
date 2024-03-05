import openai
import pytest

from chatgpt_prompts import is_urgent_assistance_needed, \
    is_intent_to_end_conversation, \
    is_assistance_needed_from_conversation_history


@pytest.mark.integration
def test_openai_version():
    assert openai.__version__ == "0.28.0"


def test_is_urgent_assistance_needed():
    assert (is_urgent_assistance_needed("Hi ChatGPT")) is not True
    assert (is_urgent_assistance_needed("I am tired")) is not \
           True
    assert (is_urgent_assistance_needed("I fell down")) is True
    assert (is_urgent_assistance_needed("I need my medication")) is True
    assert (is_urgent_assistance_needed("Ahh my chest hurts and I can't breath"
                                        )) is True


def test_is_intent_to_end_conversation():
    assert (is_intent_to_end_conversation("Hi ChatGPT")) is not True
    assert (is_intent_to_end_conversation("GoodBye")) is True
    assert (is_intent_to_end_conversation("I don't want to talk anymore")) \
           is True


def test_is_assistance_needed_from_conversation_history():

    conversation_history = [
        {
            "role": "user",
            "content": "Good morning CareBot!"
        },
        {
            "role": "assistant",
            "content": "Good morning! How can I assist you today?"
        },

    ]

    resident_input = "I going great and I don't need help. Goodbye For now"
    assert is_assistance_needed_from_conversation_history(resident_input,
                                                          conversation_history
                                                          ) is not True

    conversation_history2 = [
        {
            "role": "user",
            "content": "CareBot I am not feeling good today!"
        },
        {
            "role": "assistant",
            "content": "I'm sorry to hear that how can I help?"
        },

    ]
    resident_input2 = "I'm in a lot of pain and I require a nurse"
    assert is_assistance_needed_from_conversation_history(resident_input2,
                                                          conversation_history2
                                                          ) is True

import openai
import pytest

from chatgpt_prompts import is_urgent_assistance_needed, \
    is_intent_to_end_conversation


@pytest.mark.smoke
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
    assert(is_intent_to_end_conversation("GoodBye")) is True
    assert (is_intent_to_end_conversation("I don't want to talk anymore")) \
           is True

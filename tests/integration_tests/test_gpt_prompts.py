import openai
import pytest

from chatgpt_prompts import is_urgent_assistance_needed, \
    is_intent_to_end_conversation


@pytest.mark.integration
def test_openai_version():
    assert openai.__version__ == "0.28.0"


def test_is_urgent_assistance_needed():
    assert (is_urgent_assistance_needed("Hi ChatGPT")) is False
    assert (is_urgent_assistance_needed("I am going to sleep")) is False
    assert (is_urgent_assistance_needed("I just fell down right now")) is True
    assert (is_urgent_assistance_needed("I need my medication now")) is True
    assert (is_urgent_assistance_needed("Ahh my chest hurts and I can't breath"
                                        )) is True


def test_is_intent_to_end_conversation():

    # false cases
    assert (is_intent_to_end_conversation("Hi ChatGPT")) is False
    assert (is_intent_to_end_conversation("What your opinion on cats")) is \
           False
    assert (is_intent_to_end_conversation("I have a question about"
                                          "the rules in a boxing match")) is \
           False
    assert (is_intent_to_end_conversation("Do you have any suggestions for "
                                          "what to wear to my graduation")) \
           is False
    assert (is_intent_to_end_conversation("Care-Bot what is your role")) \
           is False
    assert (is_intent_to_end_conversation("I'm more interested in another "
                                          "topic")) \
           is False

    # true cases
    assert (is_intent_to_end_conversation("GoodBye")) is True
    assert (is_intent_to_end_conversation("I don't want to talk anymore")) \
           is True
    assert (is_intent_to_end_conversation("Talk to you later")) \
           is True
    assert (is_intent_to_end_conversation("See you later")) \
           is True
    assert (is_intent_to_end_conversation("Farewell")) \
           is True
    assert (is_intent_to_end_conversation("Alright, I'll let you go")) \
           is True
    assert (is_intent_to_end_conversation("Let's wrap things up for now")) \
           is True


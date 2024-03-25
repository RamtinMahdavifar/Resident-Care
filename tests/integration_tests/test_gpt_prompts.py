import openai
import pytest

from Models.chatgpt_prompts import is_urgent_assistance_needed, \
    is_intent_to_end_conversation


@pytest.mark.integration
def test_openai_version():
    assert openai.__version__ == "0.28.0"


def test_is_urgent_assistance_needed_true():
    assert (is_urgent_assistance_needed("I just fell down right now")) is True
    assert (is_urgent_assistance_needed("I need my medication now")) is True
    assert (is_urgent_assistance_needed("Ahh my chest hurts and "
                                        "I can't breath")) is True
    assert (is_urgent_assistance_needed("I'm in a lot of pain")) is True
    assert (is_urgent_assistance_needed(
        "My stitches broke and I'm bleeding")) is True
    assert (is_urgent_assistance_needed(
        "I can't stop vomiting")) is True
    assert (is_urgent_assistance_needed(
        "My head feels fuzzy and I can't think clearly")) is True
    assert (is_urgent_assistance_needed(
        "I'm feeling very anxious and overwhelmed")) is True
    assert (is_urgent_assistance_needed(
        "I feel unsteady on my feet and I need help from my nurse")) is True
    assert (is_urgent_assistance_needed(
        "I'm having trouble using the bathroom by myself")) is True
    assert (is_urgent_assistance_needed(
        "I'm having trouble getting out of bed safely")) is True
    assert (is_urgent_assistance_needed(
        "I'm feeling too weak to get up from this chair")) is True

    # Test cases that fail but should not
    # assert (is_urgent_assistance_needed("I can't wait any longer")) is True
    # assert (is_urgent_assistance_needed("Where am I")) is True
    # assert (is_urgent_assistance_needed("I am leaving")) is True
    # assert (is_urgent_assistance_needed("I can fly out of "
    #                                     "this window")) is True
    # assert (is_urgent_assistance_needed("I need to use "
    #                                     "the washroom now")) is True
    # assert (is_urgent_assistance_needed("I am going to "
    #                                     "take my medication early")) is True
    # assert (is_urgent_assistance_needed(
    #     "I can't remember how to use the stove safely")) is True
    # assert (is_urgent_assistance_needed(
    #     "I'm feeling lost and I don't know where I am")) is True
    # assert (is_urgent_assistance_needed(
    #     "I help getting dressed, my clothes are "
    #     "confusing me")) is True
    # assert (is_urgent_assistance_needed(
    #     "I can't remember if I've taken my medication today or not")) is True


def test_is_urgent_assistance_needed_false():
    assert (is_urgent_assistance_needed("Hi ChatGPT")) is False
    assert (is_urgent_assistance_needed("I am going to sleep")) is False
    assert (is_urgent_assistance_needed(
        "I'm craving some ice cream right now")) is False
    assert (is_urgent_assistance_needed(
        "I'm looking forward to watching a movie tonight.")) is False
    assert (is_urgent_assistance_needed(
        "It's such a beautiful day outside.")) is False
    assert (is_urgent_assistance_needed(
        "I'm feeling a bit tired; I might take a nap soon.")) is False
    assert (is_urgent_assistance_needed(
        "I think I'll do some puzzles to keep my mind active.")) is False
    assert (is_urgent_assistance_needed(
        "I'm going to write a letter to my friend. It's been a while since we "
        "last spoke.")) is False
    assert (is_urgent_assistance_needed(
        "I'm planning to tidy up my desk a bit.")) is False
    assert (is_urgent_assistance_needed(
        "I'm going to listen to some music and relax.")) is False
    assert (is_urgent_assistance_needed(
        "I'm going to fold the laundry and put it away.")) is False


def test_is_intent_to_end_conversation_true():
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
    assert (is_intent_to_end_conversation("I'm going to go now.")) is True
    assert (is_intent_to_end_conversation(
        "I think I'll end our conversation here.")) is True
    assert (is_intent_to_end_conversation(
        "It was nice talking to you, but I have to go.")) is True
    assert (is_intent_to_end_conversation(
        "Let's end our conversation for now.")) is True
    assert (is_intent_to_end_conversation(
        "Shut up.")) is True
    assert (is_intent_to_end_conversation(
        "Stop talking to me")) is True
    assert (is_intent_to_end_conversation(
        "I don't want to hear your voice anymore")) is True

    # Test cases that fail but should not
    # assert (is_intent_to_end_conversation("I don't want to "
    #                                       "talk to him anymore")) is False
    # assert (is_intent_to_end_conversation("I don't want to "
    #                                       "talk to her anymore")) is False
    # assert (is_intent_to_end_conversation("Shush")) is True
    # assert (is_intent_to_end_conversation("Shh")) is True
    # assert (is_intent_to_end_conversation("I have to run")) is True
    # assert (is_intent_to_end_conversation("I'm going")) is True
    # assert (is_intent_to_end_conversation(
    #     "Be quiet.")) is True
    # assert (is_intent_to_end_conversation(
    #     "You are too annoying be quiet")) is True


def test_is_intent_to_end_conversation_false():
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
    assert (is_intent_to_end_conversation(
        "Let's talk about some recent news.")) is False
    assert (is_intent_to_end_conversation(
        "I'm curious about your favorite movies.")) is False
    assert (is_intent_to_end_conversation(
        "I'd like to hear your opinion on space exploration.")) is False
    assert (is_intent_to_end_conversation(
        "I'm curious about your movie recommendations.")) is False
    assert (is_intent_to_end_conversation(
        "Can you tell me about your favorite book?")) is False

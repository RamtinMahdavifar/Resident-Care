import openai
import pytest

from chatgpt_prompts import is_urgent_assistance_needed


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

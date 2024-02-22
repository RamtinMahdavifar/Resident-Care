import openai
import pytest

from chatgpt_prompts import generate_response


@pytest.mark.smoke
def test_openai_version():
    assert openai.__version__ == "0.28.0"


def test_gpt_response():
    assert len(generate_response("Hi ChatGPT", [])) != 0

import os
import openai
from dotenv import load_dotenv

# Set your OpenAI GPT API key
openai.api_key = "YOUR_OPENAI_API_KEY"

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def generate_response(input_text, conversation_history, prompt_number):
    """
    Generate a response to the input text using OpenAI's GPT model.

    Parameters:
    input_text (str): The user's input text to respond to.
    conversation_history (list): The history of the conversation.

    Returns:
    str: The generated response text.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant and need to figure out if a hospital or nursing \
            home resident requires assistance. Always ask if they need assistance at the end"},
    ]

    messages.extend(conversation_history)
    messages.append({"role": "user", "content": input_text})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=1.3,
    )

    response_text = response['choices'][0]['message']['content']

    conversation_history.append({"role": "user", "content": input_text})
    conversation_history.append({"role": "assistant", "content": response_text})

    return response_text




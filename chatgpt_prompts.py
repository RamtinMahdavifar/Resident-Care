import os

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def append_conversation_history(input_text, response_text,
                                conversation_history):
    """
    Append the user's input and the assistant's response to the conversation
    history.

    This function modifies the conversation history in place by adding
    two new entries: one for the user's input and one for the
    assistant's response.

    Parameters:
        - input_text (str): The user's input text.
        - response_text (str): The assistant's generated response text.
        - conversation_history (list): The history of the conversation to which
          the new interaction will be appended. Each item in the list is a
          dict with 'role' (either 'user' or 'assistant') and 'content' keys.

    Returns:
        - None
    """
    conversation_history.append({"role": "user", "content": input_text})

    conversation_history.append({
        "role": "assistant",
        "content": response_text
    })


def generate_response(input_text,
                      conversation_history,
                      is_save_conversation_history=True):
    """
    Generate a response to the input text using OpenAI's GPT model and
    optionally append the interaction to the conversation history.

    Parameters:
        - input_text (str): The user's input text to respond to.
        - conversation_history (list): The history of the conversation, each
          item being a dict with 'role' and 'content' keys.
        - is_save_conversation_history (bool, optional): Flag indicating
          whether to save this interaction (input and response) to the
          conversation history. Defaults to True.

    Returns:
        - str: The generated response text.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant and need \
        to figure out if a hospital or nursing home resident requires \
        assistance. Always ask if they need assistance at the end"},
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

    if is_save_conversation_history:
        append_conversation_history(input_text,
                                    response_text,
                                    conversation_history)

    return response_text


def summarize_conversation_history(conversation_history):
    """
    Summarizes conversation history with chat GPT in a short concise manner

    Parameters:
    input_text (str): The user's input text to respond to.
    conversation_history (list): The history of the conversation.

    Returns:
        -str: The generated response text.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant for a \
                                      hospital or nursing  home resident. \
                                      You directly interact with the \
                                      resident and you must summarize the \
                                      conversation history  that you had \
                                      with the resident"},
    ]

    input_text = "Summarize the conversation history you had with the  \
                 resident in clear concise and nicely formatted  manner. \
                 This information will be sent to a nurse or caregiver."

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
    conversation_history.append(
        {"role": "assistant", "content": response_text})

    return response_text

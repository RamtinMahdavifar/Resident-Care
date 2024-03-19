import os
import sys
from typing import Optional, Any

import openai
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Resident details fetching should be corrected as follows:
g_resident_first_name: Optional[str] = os.getenv('RESIDENT_FIRST_NAME')
g_resident_last_name: Optional[str] = os.getenv('RESIDENT_LAST_NAME')
g_resident_age_years_str: Optional[str] = os.getenv('RESIDENT_AGE_YEARS')
g_resident_sex: Optional[str] = os.getenv('RESIDENT_SEX')
g_resident_medical_conditions: Optional[str] = os.getenv(
    'RESIDENT_MEDICAL_CONDITIONS')

# Validate g_resident_first_name and g_resident_last_name are non-empty strings
if not g_resident_first_name or not g_resident_last_name:
    print("Error: Resident first name and last name must be non-empty "
          "strings.")
    sys.exit(1)

# Validate g_resident_age_years is an integer between 1-130
try:
    if g_resident_age_years_str is None:
        raise ValueError("Age is not set.")
    g_resident_age_years = int(g_resident_age_years_str)
    if not 1 <= g_resident_age_years <= 130:
        raise ValueError("Age must be between 1 and 130.")
except ValueError as e:
    print(f"Error: Invalid age - {e}")
    sys.exit(1)

# Validate g_resident_sex is either "Male" or "Female" (case-insensitive)
if g_resident_sex is None or g_resident_sex.lower() not in ["male", "female"]:
    print("Error: Resident sex must be either 'Male' or 'Female'.")
    sys.exit(1)

# If all validations pass, you can continue with your program logic
print("All Resident input data is valid.")


def append_conversation_history(
        input_text: str,
        response_text: str,
        conversation_history: List[Dict[str, str]]
) -> None:
    """
    Append the user's input and the assistant's response to the conversation
    history if they are not empty.

    This function modifies the conversation history in place by adding
    two new entries: one for the user's input and one for the
    assistant's response. The entries are only added if they are not empty.

    Parameters:
        - input_text (str): The user's input text.
        - response_text (str): The assistant's generated response text.
        - conversation_history (list): The history of the conversation to which
          the new interaction will be appended. Each item in the list is a
          dict with 'role' (either 'user' or 'assistant') and 'content' keys.

    Returns:
        - None
    """
    if len(input_text) != 0:
        conversation_history.append({"role": "user", "content": input_text})

    if len(response_text) != 0:
        conversation_history.append({
            "role": "assistant",
            "content": response_text
        })


def generate_response(
        input_text: str,
        conversation_history: List[Dict[str, str]],
        is_save_conversation_history: bool = True,
        is_function_call=False
        # Make function_call optional
) -> str:
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
        {"role": "system", "content": "You are a helpful assistant named "
                                      "Care-Bot. Your duty is to assist\
        hospital or nursing home Residents. You responsibilities include \
        conversing with the Resident, determining if they require urgent "
                                      "assistance, determining if the Resident"
                                      "has the intend to end the conversation"
                                      "while conversing and summarizing "
                                      "conversation history to be sent to a"
                                      "Caregiver. Do not return any emojis in"
                                      "the response. Only return back text"},
    ]

    messages.extend(conversation_history)
    messages.append({"role": "user", "content": input_text})

    function_call = {
        "name": "check_urgency",
        "description": "Return true if you think the resident requires urgent assistance based on the ontext if input text otherwise return false",
        "parameters": {
            "type": "object",
            "properties": {
                "type": "string",
                "input_text": input_text
            }

        }
    }

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=1.3,
        functions=[function_call]
    )

    response_text = response['choices'][0]['message']['content']

    if is_save_conversation_history:
        append_conversation_history(input_text,
                                    response_text,
                                    conversation_history)

    return response_text


def is_urgent_assistance_needed(input_text: str) -> bool:
    """
    Determines whether the input text indicates a situation where urgent
    assistance is needed.

    This function constructs a function call to assess the urgency of assistance
    required based on the input text.

    Parameters:
    - input_text (str): Text describing a situation involving a Resident,
    which is to be evaluated for urgency.

    Returns:
    - bool: True if urgent assistance is needed, False otherwise.
    """

    # Generate response from ChatGPT
    response = generate_response("Is urgent assistance needed?", [],
                                 False)

    # Interpret the response
    if "true" in response.lower():
        return True
    elif "false" in response.lower():
        return False
    else:
        # If the response is not clear, return False
        return False


def is_assistance_needed_from_conversation_history(
        input_text: str,
        conversation_history: List[Dict[str, str]]
) -> bool:
    """
       Determines whether assistance is needed based on the last 1-3 messages
       in the conversation history between a Resident and the System.

       This function reviews the last 1-3 messages in the conversation history
       to identify if they indicate a situation where the Resident requires
       assistance.
       It appends the latest input text to the conversation history and uses
       a prompt to analyze the conversation context. Based on the analysis, it
       generates a response indicating whether assistance is needed (true) or
       not (false).

       Parameters:
       - input_text (str): The latest message from the Resident, to be
        appended to the conversation history for context analysis.
       - conversation_history (list): A list of dictionaries, each
         representing a message in the conversation history. Each dictionary
         contains two keys: "role" (indicating
         whether the message is from the "user" or "assistant") and
         "content" (the message text).

       Returns:
       - bool: True if the analysis of the conversation history indicates that
        the Resident requires assistance, False otherwise.
       """
    prompt = "Reply back true if the last 1-3 messages in the " \
             "conversation_history indicates a situation " \
             "where the Resident requires assistance." \
             "Otherwise reply " \
             "back false. Only Reply true or false, do not respond back " \
             "with " \
             "anything else."

    temp_convo_history = conversation_history
    append_conversation_history(input_text, "", temp_convo_history)
    response = generate_response(prompt, temp_convo_history, False)

    if "true" in response.lower():
        return True
    else:
        return False


def is_intent_to_end_conversation(input_text: str) -> bool:
    """
    Determines whether the input text indicates an intent by the Resident
    to end the conversation, based on the response from a generated response
    function.

    This function constructs a prompt that asks whether the provided input text
    signifies an intent by the Resident to conclude the conversation. Examples
    of such intent include phrases like "goodbye", "I don't want to talk to
    you anymore", and "no, thanks bye". The function then interprets a
    response containing the string "true", in a case-insensitive manner, as an
    indication that the intent is indeed to end the conversation.

    Parameters:
    - input_text (str): Text that is being evaluated for signs of intent to
        end the conversation.

    Returns:
    - bool: True if the generated response suggests an intent to end the
        conversation,
        False otherwise.
    """
    prompt = "Reply back true if the Input Text below " \
             "indicate if the Resident has the indent to end the " \
             "conversation. Otherwise reply back false" \
             "" \
             "An examples of the intend to end conversation " \
             "are goodbye, I don't want to talk to you anymore, " \
             "no thanks bye." \
             "Only Reply true or false, do not respond back " \
             "with " \
             "anything else. " \
             "Input Text: " + input_text
    response = generate_response(prompt, [], False)
    if "true" in response.lower():
        return True
    else:
        return False


def summarize_conversation_history(conversation_history: List[Dict[str, str]]
                                   ) -> str:
    """
    Summarizes conversation history with chat GPT in a short concise manner

    Parameters:
    input_text (str): The user's input text to respond to.
    conversation_history (list): The history of the conversation.

    Returns:
        -str: The generated response text.
    """

    prompt = "Summarize the conversation history you had with the  \
                 Resident in clear concise and nicely formatted  manner. \
                 This information will be sent to a nurse or caregiver"

    return generate_response(prompt, conversation_history, False)


print(generate_response("hi ", [], False, False))
import re


def check_for_assistance(text):
    """
    Check if the given text contains keywords indicative of a request for
    assistance or emergency.

    Parameters:
    text (str): The input text to analyze for assistance-related keywords.

    Returns:
    bool: True if assistance-related keywords are found, False otherwise.
    """
    pattern = re.compile(
        r'\b(?:Help|Emergency|Fall('
        r'?:en|ing)?|Hurt|Medication|Doctor|Nurse|Sick|Assistance|Aid'
        r'|Distress|Panic|Suffering|Support|Alarming|Disturbance|Critical'
        r'|Rescue|Urgent|Quick|Ache|Trouble|Need|Now|Bad|Unwell|Worsen('
        r'?:ing)?|Stop|Difficult|Terrible|Worse|Abnormal|Unbearable|Concern'
        r'|Serious|Intense|Dire|Dangerous|Frantic|Dreadful|Panic('
        r'?:king)?|Fright(?:en(?:ing|ed)?)?|Terrify(?:ing)?|Urgency|Agon('
        r'?:y|izing)|Mis(?:ery|erable)|Worr(?:y|ied)|Pain(?:ful)?)(?:s|es)?\b',
        re.IGNORECASE)
    return bool(pattern.search(text))

import pytest

from keyword_recognition import has_keyword

keywords = [
    "Help", "Emergency", "Fall", "Hurt", "Medication", "Doctor", "Nurse",
    "Sick", "Assistance", "Aid", "Distress", "Panic", "Suffering", "Support",
    "Alarming", "Disturbance", "Critical", "Rescue", "Urgent", "Quick",
    "Ache", "Trouble", "Need", "Now", "Bad", "Unwell", "Worsen", "Stop",
    "Difficult", "Terrible", "Worse", "Abnormal", "Unbearable", "Concern",
    "Serious", "Intense", "Dire", "Dangerous", "Frantic", "Dreadful",
    "Fright", "Terrify", "Urgency", "Agony", "Agonizing", "Misery",
    "Miserable", "Worry", "Worried", "Painful", "Pain", "Care", "Bot",
    "CareBot"
]


@pytest.mark.unit
def test_has_keyword_on_all_keywords():
    """
     Tests whether the has_keyword function correctly identifies the presence
     of each keyword in a list of predefined keywords.

     This test iterates over each keyword and asserts that has_keyword returns
     True, indicating the keyword is recognized as significant by the
     function.

     If any keyword is not correctly recognized, the test fails, specifying
     which keyword failed.
     """
    for word in keywords:
        assert has_keyword(word) is True, f"Keyword failed: {word}"


def test_has_keyword_on_sentences_with_keywords():
    """
      Tests whether the has_keyword function can accurately detect the presence
      of keywords within various sentence structures.

      This test constructs sentences by inserting predefined keywords into
      sentence templates at different positions (start, middle, end) and with
      varying counts of placeholders for keywords (one to three).

      It asserts that has_keyword recognizes the presence of keywords in these
      sentences, failing the test with specific feedback if any sentence does
      not trigger the expected True response from has_keyword.

      Sentence templates include scenarios with a single keyword, two keywords,
      and three keywords to ensure robust keyword detection across different
      contexts.
      """
    # Define a list of template sentences with placeholders for keywords
    sentence_templates = [
        "{} needed urgently.",
        "Please {}, I need assistance.",
        "I don't feel well, might {} soon.",
        "Can someone {}?",
        "Feeling {} and need help.",
        "This is an {} situation.",
        "In case of {}, do this.",
        "{}! This is serious.",
        "I need {} and support.",
        "The situation is getting {}.",
        "Experiencing {} pain and discomfort.",
        "{} and {} are both required immediately.",
        "{} I need {} it's {}"
    ]

    # Loop through the sentence templates
    for template in sentence_templates:
        # Insert each keyword into the sentence placeholder(s)
        for keyword in keywords:
            placeholders_count = template.count("{}")
            try:
                if placeholders_count == 1:
                    # For templates with a single placeholder
                    sentence = template.format(keyword)
                elif placeholders_count == 2:
                    # For templates expecting two placeholders
                    sentence = template.format(keyword, keyword)
                elif placeholders_count == 3:
                    # For templates expecting three placeholders
                    sentence = template.format(keyword, keyword, keyword)
                else:
                    raise ValueError(
                        "Template with unexpected number of placeholders.")

                # Call the check_for_assistance function with the filled
                # sentence
                result = has_keyword(sentence)

                # Assert that the result is True, as we expect keywords to
                # trigger a True response
                assert result, f"Failed for sentence: {sentence}"
            except Exception as e:
                print(
                    f"Error processing sentence template '{template}' with "
                    f"keyword '{keyword}': {e}")


def test_has_keyword_on_non_keywords():
    """
    Tests the has_keyword function on words that are not defined as keywords
    to ensure it accurately returns False for non-keyword inputs.
    """
    # List of words that are not considered as keywords.
    non_keywords = ["hello", "sad", "goodbye", "friend", "walk", "play",
                    "music","dinner", "book", "computer", "phone", "table",
                    "chair", "sleepy"]

    # Loop through the non-keywords list and test each with has_keyword
    for word in non_keywords:
        result = has_keyword(word)
        assert not result, f"Non-keyword detected as keyword: {word}"

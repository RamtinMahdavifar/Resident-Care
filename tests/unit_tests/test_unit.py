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
    for word in keywords:
        assert has_keyword(word) is True

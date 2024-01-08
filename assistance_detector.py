import re

def check_for_assistance(text):
    pattern = re.compile(r'\b(?:help|assistance|emergency|urgent|pain|hurt|fall(?:en)?|accident|trouble|not feeling well|sick|medicine|doctor|nurse|can\'t get up|need someone|come quickly|help me please|I need help|it\'s an emergency|I\'ve fallen and I can\'t get up|I\'m in pain|I need my medication|I feel sick|I need a doctor|something\'s wrong|carebot)\b', re.IGNORECASE)
    return bool(pattern.search(text))

# textutilsSohaib/transformations.py

import string

def to_uppercase(_text):
    """Converts all characters in the text to uppercase."""
    return _text.upper()

def to_lowercase(_text):
    """Converts all characters in the text to lowercase."""
    return _text.lower()

def reverse_text(_text):
    """Reverses the input text."""
    return _text[::-1]

def capitalize_words(_text):
    """Capitalizes the first letter of each word in the text."""
    return _text.title()

def remove_whitespace(_text):
    """Removes all whitespace characters from the text."""
    return _text.replace(" ", "")

def word_count(_text):
    """Returns the number of words in the text."""
    return len(_text.split())

def replace_spaces_with_underscore(_text):
    """Replaces spaces with underscores in the text."""
    return _text.replace(" ", "_")

# New Enhancements for version 1.1.0

def remove_punctuation(_text):
    """Removes punctuation characters from the text."""
    return _text.translate(str.maketrans("", "", string.punctuation))

def reverse_words(_text):
    """Reverses the order of words in the text."""
    return " ".join(reversed(_text.split()))

def count_vowels(_text):
    """Counts the number of vowels (a, e, i, o, u) in the text."""
    vowels = "aeiouAEIOU"
    return sum(1 for char in _text if char in vowels)

def is_palindrome(_text):
    """Checks if the text is a palindrome."""
    _text = _text.lower().replace(" ", "")  # Remove spaces and convert to lowercase
    return _text == _text[::-1]

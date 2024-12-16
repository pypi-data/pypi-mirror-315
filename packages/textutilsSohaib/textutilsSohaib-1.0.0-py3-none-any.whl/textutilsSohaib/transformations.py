# textutilsSohaib/transformations.py

def to_uppercase(text):
    """
    Converts a string to uppercase.
    """
    return text.upper()

def to_lowercase(text):
    """
    Converts a string to lowercase.
    """
    return text.lower()

def reverse_text(text):
    """
    Reverses the given string.
    """
    return text[::-1]

def capitalize_words(text):
    """
    Capitalizes the first letter of each word in the string.
    """
    return text.title()

def remove_whitespace(text):
    """
    Removes leading and trailing whitespace from the string.
    """
    return text.strip()

def word_count(text):
    """
    Returns the count of words in the string.
    """
    return len(text.split())

def replace_spaces_with_underscore(text):
    """
    Replaces spaces in the string with underscores.
    """
    return text.replace(" ", "_")

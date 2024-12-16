def to_uppercase(text):
    """Converts a string to uppercase."""
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    return text.upper()

def to_lowercase(text):
    """Converts a string to lowercase."""
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    return text.lower()

def reverse_text(text):
    """Reverses the string."""
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    return text[::-1]

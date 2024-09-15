# helpers/utils.py

import secrets
import string


def generate_secure_random_string(length):
    """
    Generates a cryptographically secure random string of specified length.

    Parameters:
    - length (int): The length of the random string to generate.

    Returns:
    - str: A secure random string of the specified length.
    """
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Length must be a positive integer.")

    characters = string.ascii_letters + string.digits
    # characters += string.punctuation  # Uncomment to include special characters

    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

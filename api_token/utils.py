def generate_token() -> str:
    """
    Generates a new token of 25 characters long

    :return: a string token
    """
    import string
    import secrets

    alphabet = string.ascii_letters + string.digits

    while True:
        token = ''.join(secrets.choice(alphabet) for i in range(25))
        if any(c.islower() for c in token) and any(c.isupper() for c in token) and sum(
                c.isdigit() for c in token) >= 10:
            # if the new token contain 10 alphabets and at least 1 lowercase character
            return token

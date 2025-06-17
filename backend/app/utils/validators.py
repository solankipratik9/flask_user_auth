import re
from email_validator import validate_email as email_validate, EmailNotValidError


def validate_email(email):
    """Validate email format."""
    try:
        valid = email_validate(email)
        return True
    except EmailNotValidError:
        return False


def validate_password(password):
    """Validate password strength."""
    if len(password) < 8:
        return False

    # Check for at least one uppercase, one lowercase, one digit
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False

    return True


def validate_uuid(uuid_string):
    """Validate UUID format."""
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False

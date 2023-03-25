from email_validator import validate_email, EmailNotValidError


def check_email(email):
    """Checks if an email is valid
    Args:
        email (str): user's email address
    Returns:
        (True, ''): normalized email if it is valid
        (False, error): error message if it is invalid
    """
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError as e:
        return False, str(e)

    return True, ''


def check_password(password):
    """Checks if a password is valid
    Args:
        password (string): user's password
    Returns:
        (True, ''): password if it is valid
        (False, error): error message if it is invalid
    """

    # Is at least 8 characters long
    if len(password) < 8:
        return False, 'Password must have at least 8 characters.'
    # Contains a number
    if not any(c.isdigit() for c in password):
        return False, 'Password must contain a number.'
    # Contains an uppercase character
    if not any(c.isupper() for c in password):
        return False, 'Password must contain an uppercase character.'
    # Contains a lowercase character
    if not any(c.islower() for c in password):
        return False, 'Password must contain a lowercase character.'

    return True, ''


def valid_login(req):
    """Checks if login is valid
    Args:
        req (JSON): contains email and password strings
    Returns:
        is_valid: whether the email and password are valid
        errors: dictionary of email and/or password errors
    """
    errors = {
        'email': '',
        'password': ''
    }

    is_valid = True
    if req['email'] == '':
        is_valid = False
        errors['email'] = 'Email must not be left blank'
    if req['password'] == '':
        is_valid = False
        errors['password'] = 'Password must not be left blank'

    return is_valid, errors


def valid_registration(req):
    """Checks if registration is valid
    Args:
        req (JSON): contains email and password strings
    Returns:
        is_valid: whether the email and password are valid
        errors: dictionary of email and/or password errors
    """
    errors = {
        'email': '',
        'password': ''
    }

    is_valid_email, email_error = check_email(req['email'])
    is_valid_password, password_error = check_password(req['password'])

    is_valid = True
    if not is_valid_email:
        is_valid = False
        errors['email'] = email_error
    if not is_valid_password:
        is_valid = False
        errors['password'] = password_error

    return is_valid, errors

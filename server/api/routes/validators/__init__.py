def parse_error(e):
    """Parses a ValidationError object
    Args:
        e (ValidationError): error given from mongoengine
    Returns:
        dict: error messages from e
    """
    errors = dict()
    if e.errors:
        for field in e.errors:
            errors[field] = e.errors[field]._message
    else:
        errors['msg'] = e._message
    return errors

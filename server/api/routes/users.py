from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from api import bcrypt
from database import User
from api.routes.validators.users import valid_login, valid_registration

users = Blueprint('users', __name__)


@users.route('/login', methods=['POST'])
def login():
    """POST users/login
    Desc: Logs in a user
          Checks if any fields are blank
          Checks if an account exists at all
          Checks if an account exists and the password was incorrect
    Returns:
        200: authentication token
        401: password was incorrect, unauthorized access
        404: no account was found or field was empty
    """
    req = request.get_json()
    is_valid, errors = valid_login(req)
    if not is_valid:
        return errors, 404

    user = User.objects(email=req['email']).first()
    if not user:
        return {
            'email': 'No account with this email exists.',
            'password': ''
        }, 404
    if not bcrypt.check_password_hash(user.password, req['password']):
        return {
            'email': '',
            'password': 'Password is incorrect.'
        }, 401

    access_token = create_access_token(identity=user)
    return {
        'token': access_token
    }, 200


@users.route('/register', methods=['POST'])
def register():
    """POST users/register
    Desc: Registers a new user
          Validates email and password used to register
          Ensures new accounts are not duplicates
    Returns:
        201: authentication token
        401: validation error, unauthorized access
        409: duplicate account, conflict with database
    """
    req = request.get_json()
    is_valid, errors = valid_registration(req)
    if not is_valid:
        return errors, 401

    user = User.objects(email=req['email']).first()
    if user:
        return {
            'email': 'Account could not be created. User already exists.',
            'password': ''
        }, 409

    new_user = User(**req)
    pw_hash = bcrypt.generate_password_hash(new_user.password).decode('utf-8')
    new_user.password = str(pw_hash)
    new_user.save()

    access_token = create_access_token(identity=new_user)
    return {
        'token': access_token
    }, 201
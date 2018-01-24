import uuid, json, decimal, datetime, jwt
from flask import Blueprint, request, jsonify, make_response
from app.models.user import User
from app.models.role import Role
from app import db, bcrypt, secret_key
from functools import wraps
from app.utils.auth import token_required

mod_auth_api = Blueprint('auth', __name__, url_prefix='/api')

@mod_auth_api.route('/auth', methods=['POST'])
def auth():
    # Getting the json data in request
    data = request.get_json()

    # If username or password not provided
    if data == {}:
        return {'message': 'Username or password is invalid!'}

    # Finding user by username or email
    if '@' in data['username_email'].strip():
        user = User.query.filter_by(email_address=data['username_email'].strip()).first()
    else:
        user = User.query.filter_by(username=data['username_email'].strip()).first()

    # If user not found
    if not user:
        return jsonify({'message': 'Username or Email is invalid!'})

    # Checking password
    if bcrypt.check_password_hash(user.password, data['password']):
        # If user is active give the token
        if user.active:
            token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)}, secret_key)

            return jsonify({'message': 'Successfully login', 'token': token.decode('UTF-8'), 'role': user.role.name})
        return jsonify({'message': 'User is not activated!'})

    # if password is wrong
    return jsonify({'message': 'Password is invalid!'})

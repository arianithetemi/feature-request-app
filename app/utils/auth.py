import jwt
from flask import request, jsonify, g
from app.models.user import User
from functools import wraps
from app import secret_key

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, secret_key)
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def role_required(role):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            try:
                data = jwt.decode(token, secret_key)
                current_user = User.query.filter_by(public_id=data['public_id']).first()
            except:
                return jsonify({'message': 'Token is invalid!'}), 401

            print current_user.role.name
            print role
            if current_user.role.name != role:
                return jsonify({'message': 'Permission denied!'}), 401

            return f(*args, **kwargs)
        return wrapped
    return wrapper

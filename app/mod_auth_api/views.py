import uuid, json, decimal, datetime, jwt
from flask import Blueprint, request, jsonify, make_response
from app.models.user import User
from app.models.role import Role
from app import db, bcrypt
from functools import wraps

mod_auth_api = Blueprint('auth', __name__, url_prefix='/api')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, 'thisisthesecretkey')
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@mod_auth_api.route('/auth', methods=['POST'])
def auth():
    # Getting the json data in request
    data = request.get_json()

    # If username or password not provided
    if not data:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    # Finding user by username
    user = User.query.filter_by(username=data['username']).first()

    # If user not found
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    # Checking password
    if bcrypt.check_password_hash(user.password, data['password']):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'thisisthesecretkey')

        return jsonify({'token': token.decode('UTF-8'), 'role': user.role.name})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

@mod_auth_api.route('/dashboard', methods=['GET'])
@token_required
def dashboard(current_user):
    
    return jsonify({'message': 'Successfully login'})

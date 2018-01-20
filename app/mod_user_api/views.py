import uuid, json, decimal, datetime
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.role import Role
from app import db, bcrypt

mod_user_api = Blueprint('user_api', __name__, url_prefix='/api/user')

@mod_user_api.route('/', methods=['GET'])
def get_users():
        # Gell all users from db
        users = User.query.all()

        # Building JSON for each user and append to array
        output = []
        for user in users:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['first_name'] = user.first_name
            user_data['last_name'] = user.last_name
            user_data['username'] = user.username
            user_data['email_address'] = user.email_address
            user_data['role'] = user.role.name
            user_data['active'] = user.active
            output.append(user_data)

        # Returning array of users in json
        return jsonify({'users': output})

@mod_user_api.route('/add', methods=['POST'])
def add_user():
    # Getting json data from request
    data = request.get_json()

    # Hashing password
    hash_password = bcrypt.generate_password_hash(data['password'])

    # Creating instance of new user with json data values
    user = User(public_id=str(uuid.uuid4()), first_name=data['first_name'], last_name=data['last_name'], username=data['username'], active=False, email_address=data['email_address'], password=hash_password)

    # Setting description of the role
    description = ''
    if data['role'] == 'admin':
        description = "Administrator to manage clients, feature requests and message to client."
    else:
        description = "Client can send feature requests and start send messages."

    # Creating instance of role and set to this user
    role = Role(name=data['role'], description=description, user=user)

    # Executing queries
    db.session.add(user)
    db.session.add(role)
    db.session.commit()

    # Returning message in json
    return jsonify({'message': 'New user created!'})

@mod_user_api.route('/<public_id>', methods=['GET'])
def get_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['first_name'] = user.first_name
    user_data['last_name'] = user.last_name
    user_data['username'] = user.username
    user_data['email_address'] = user.email_address
    user_data['role'] = user.role.name
    user_data['active'] = user.active

    return jsonify({'user': user_data})

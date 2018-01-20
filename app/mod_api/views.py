import uuid, json, decimal, datetime
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.role import Role
from app import db, bcrypt

mod_api = Blueprint('api', __name__, url_prefix='/api')

@mod_api.route('/', methods=['GET'])
def index():
    ''' Renders the API index page.
    :return:
    '''
    return "Welcome to the API."

@mod_api.route('/user', methods=['GET'])
def get_all_users():

    users = User.query.all()
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

    return jsonify({'users': output})

@mod_api.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    hash_password = bcrypt.generate_password_hash(data['password'])

    new_user = User(public_id=str(uuid.uuid4()), first_name=data['first_name'], last_name=data['last_name'], username=data['username'], active=data['active'], email_address=data['email_address'], password=hash_password)

    role = Role(name='admin', description="Administrator to manage requests", user=new_user)

    db.session.add(new_user)
    db.session.add(role)
    db.session.commit()

    return jsonify({'message': 'New user created!'})

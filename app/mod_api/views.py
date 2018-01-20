import uuid
from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db, bcrypt

mod_api = Blueprint('api', __name__, url_prefix='/api')

@mod_api.route('/', methods=['GET'])
def index():
    ''' Renders the API index page.
    :return:
    '''
    return "Welcome to the API."

@mod_api.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    hash_password = bcrypt.generate_password_hash(data['password'])

    new_user = User(public_id=str(uuid.uuid4()), first_name=data['first_name'], last_name=data['last_name'], username=data['username'], email_address=data['email_address'], password=hash_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})

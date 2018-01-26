import uuid, json, decimal, datetime
from flask import Blueprint, request, jsonify, Response
from app.models.user import User
from app.models.role import Role
from app import db, bcrypt, mail
from app.utils.auth import token_required, role_required
from flask_mail import Message

mod_user_api = Blueprint('user_api', __name__, url_prefix='/api/user')

'''
    Get All Users Endpoint - Token is required
'''
@mod_user_api.route('/', methods=['GET'])
@token_required
@role_required('admin')
def get_users(current_user):
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
            user_data['company'] = user.company
            user_data['active'] = user.active
            output.append(user_data)

        # Returning array of users in json
        # return jsonify({'users': output})
        return Response(response=json.dumps(output), status=200, mimetype="application/json")

'''
    Creating New User Endpoint
'''
@mod_user_api.route('/add', methods=['POST'])
def add_user():
    # Getting json data from request
    data = request.get_json()

    if db.session.query(User).filter_by(username=data['username']).count():
        return jsonify({'message': 'Username is taken!'})

    # Checking password with confirm password
    if data['password'] != data['confirm_password']:
        return jsonify({'message': 'Password and Confirm Password do not match!'})

    # Hashing password
    hash_password = bcrypt.generate_password_hash(data['password'])

    # Creating instance of new user with json data values
    user = User(public_id=str(uuid.uuid4()), first_name=data['first_name'], last_name=data['last_name'], username=data['username'], company=data['company'], active=False, email_address=data['email_address'], password=hash_password)

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
    return jsonify({'message': 'Successfully user created!', 'status': 'inactive'})

'''
    Get One User Endpoint - Token is required
'''
@mod_user_api.route('/<public_id>', methods=['GET'])
@token_required
@role_required('admin')
def get_user(current_user, public_id):
    # query user in db by public_id
    user = User.query.filter_by(public_id=public_id).first()

    # if user not found
    if not user:
        return jsonify({'message': 'No user found!'})

    # building JSON object for found user
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['first_name'] = user.first_name
    user_data['last_name'] = user.last_name
    user_data['username'] = user.username
    user_data['email_address'] = user.email_address
    user_data['role'] = user.role.name
    user_data['active'] = user.active

    # returning user_data in json
    return jsonify({'user': user_data})

''' Activating User Endpoint - Token is required '''
@mod_user_api.route('/activate/<public_id>', methods=['PUT'])
@token_required
@role_required('admin')
def activate_user(current_user, public_id):
    # query user in db by public_id
    user = User.query.filter_by(public_id=public_id).first()

    # if user not found
    if not user:
        return jsonify({'message': 'No user found!'})

    msg = Message("IWS - Feature Request App - Account Activated",
                sender=current_user.email_address,
              recipients=[user.email_address])
    msg.html = "Hi " + user.first_name + ", <br/><br/> Your account has been successfully activated from IWS Feature Request Staff. <br/><br/> Your username is: <b>" + user.username + "</b><br/>Your password remains the same. <br/><br/> Best Regards, <br/> " + current_user.first_name + " " + current_user.last_name

    mail.send(msg)

    # Activating user in db
    user.active = True
    db.session.commit()

    return jsonify({'message': 'The user has been activated!'})

'''
    Update User Endpoint - Token is required
'''
@mod_user_api.route('/update/<public_id>', methods=['PUT'])
@token_required
def modify_user(current_user, public_id):
    # query user in db by public_id
    user = User.query.filter_by(public_id=public_id).first()

    # if user not found
    if not user:
        return jsonify({'message': 'No user found!'})

    # Getting json data from request
    data = request.get_json()

    # Checking the password
    if not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Password is invalid!'})

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email_address = data['email_address']
    user.company = data['company']
    db.session.commit()

    # building JSON object for found user
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['first_name'] = user.first_name
    user_data['last_name'] = user.last_name
    user_data['company'] = user.company
    user_data['username'] = user.username
    user_data['email_address'] = user.email_address
    user_data['role'] = user.role.name
    user_data['active'] = user.active

    # returning user_data in json
    return jsonify({'user': user_data})

'''
    Changing Password Endpoint - Token is required
'''
@mod_user_api.route('/change-password/<public_id>', methods=['PUT'])
@token_required
def change_user_password(current_user, public_id):
    # finding user with public_id
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    # Getting data
    data = request.get_json()

    # Checking password
    if not bcrypt.check_password_hash(user.password, data['current_password']):
        return jsonify({'message': 'Password is invalid!'})

    # Checking new password and confirm new password
    if data['new_password'] != data['confirm_new_password']:
        return jsonify({'message': 'New Password and Confirm New Password do not match!'})

    new_password_hash = bcrypt.generate_password_hash(data['new_password'])

    # Changing password in DB
    user.password = new_password_hash
    db.session.commit()

    return jsonify({'message': 'Password successfully changed!'})


'''
    Delete User Endpoint - Token is required
'''
@mod_user_api.route('/delete/<public_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_user(current_user, public_id):
    # finding user by public_id
    user = User.query.filter_by(public_id=public_id).first()

    # finding role of this user
    role = Role.query.filter_by(user_id=user.id).first()

    # if user not found
    if not user:
        return jsonify({'message': 'No user found!'})

    # deleting user and its role from db
    db.session.delete(user)
    db.session.delete(role)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})

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

        role = request.args.get('role')
        status = request.args.get('status')

        if status == 'True':
            final_status = True
        elif status == 'False':
            final_status = False
        else:
            final_status = None

        if role != None and final_status != None:
            users = User.query.filter_by(active=final_status).join(User.role).filter(Role.name.contains(role)).all()
        else:
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
    Creating New Client User Endpoint
'''
@mod_user_api.route('/add', methods=['POST'])
def add_user():
    # Getting json data from request
    data = request.get_json()

    if db.session.query(User).filter_by(username=data['username']).count():
        return jsonify({'message': 'Username is taken!'})

    if db.session.query(User).filter_by(email_address=data['email_address']).count():
        return jsonify({'message': 'This email is taken!'})

    # Checking password with confirm password
    if data['password'] != data['confirm_password']:
        return jsonify({'message': 'Password and Confirm Password do not match!'})

    # Hashing password
    hash_password = bcrypt.generate_password_hash(data['password'])

    # Creating instance of new user with json data values
    user = User(public_id=str(uuid.uuid4()), first_name=data['first_name'], last_name=data['last_name'], username=data['username'], company=data['company'], active=False, email_address=data['email_address'], password=hash_password)

    # Creating instance of role and set to this user
    role = Role(name='client', description="Client can send feature requests and start send messages.", user=user)

    # Executing queries
    db.session.add(user)
    db.session.add(role)
    db.session.commit()

    # Returning message in json
    return jsonify({'message': 'Successfully user created!', 'status': 'inactive'})

'''
    Creating New Admin User Endpoint
'''
@mod_user_api.route('/add/admin', methods=['POST'])
@token_required
@role_required('admin')
def add_admin(current_user):
    # Getting json data from request
    data = request.get_json()

    if db.session.query(User).filter_by(username=data['username']).count():
        return jsonify({'message': 'Username is taken!'})

    if db.session.query(User).filter_by(email_address=data['email_address']).count():
        return jsonify({'message': 'This email is taken!'})

    # Checking password with confirm password
    if data['password'] != data['confirm_password']:
        return jsonify({'message': 'Password and Confirm Password do not match!'})

    # Hashing password
    hash_password = bcrypt.generate_password_hash(data['password'])

    # Creating instance of new user with json data values
    user = User(public_id=str(uuid.uuid4()), first_name=data['first_name'], last_name=data['last_name'], username=data['username'], company=data['company'], active=True, email_address=data['email_address'], password=hash_password)

    # Creating instance of role and set to this user
    role = Role(name='admin', description="Administrator to manage clients, feature requests and message to clients.", user=user)

    msg = Message("IWS - Feature Request App - Admin Account",
                sender=current_user.email_address,
              recipients=[user.email_address])
    msg.html = "Hi " + user.first_name + ", <br/><br/> You are added as admin user in IWS Feature Request App. <br/><br/> Your username is: <b>" + user.username + "</b><br/>Your email address is: <b>"+ user.email_address +"</b><br/>Your password is  <b>"+ data['password'] +'</b>.<br /><br/> Application Link: <a href="http://'+request.host+'">'+request.host+'</a> <br/><br/> Best Regards, <br/> ' + current_user.first_name + " " + current_user.last_name + "<br/>IWS Staff member"

    mail.send(msg)

    # Executing queries
    db.session.add(user)
    db.session.add(role)
    db.session.commit()

    # Returning message in json
    return jsonify({'message': 'Successfully admin user created!', 'status': 'active'})

'''
    Get One User Endpoint - Token is required
'''
@mod_user_api.route('/<public_id>', methods=['GET'])
@token_required
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
    user_data['company'] = user.company
    user_data['active'] = user.active

    # returning user_data in json
    return jsonify({'user': user_data})

'''
    Activating User Endpoint - Token is required
'''
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
    msg.html = "Hi " + user.first_name + ", <br/><br/> Your account has been successfully activated from IWS Feature Request Staff. <br/><br/> Your username is: <b>" + user.username + "</b><br/>Your email address is: <b>"+ user.email_address +"</b><br/>Your password remains the same "+'.<br /><br/> Application Link: <a href="http://'+request.host+'">'+request.host+'</a> <br/><br/> Best Regards, <br/> ' + current_user.first_name + " " + current_user.last_name + "<br/>IWS Staff member"

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

    # Getting json data from request
    data = request.get_json()

    if user.email_address != data['email_address'] and db.session.query(User).filter_by(email_address=data['email_address']).count():
        return jsonify({'message': 'This email is taken!'})

    # if user not found
    if not user:
        return jsonify({'message': 'No user found!'})

    # Checking the password
    # if not bcrypt.check_password_hash(user.password, data['password']):
    #     return jsonify({'message': 'Password is invalid!'})

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
        return jsonify({'message': 'Current password is invalid!'})

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

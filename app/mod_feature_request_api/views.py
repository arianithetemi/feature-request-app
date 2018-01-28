import uuid, json, decimal, datetime, jwt
from flask import Blueprint, request, jsonify, make_response
from app.models.user import User
from app.models.role import Role
from app.models.client_request import ClientRequest
from app.models.correspondence import Correspondence
from app.models.messages import Message
from app import db, bcrypt, secret_key
from app.utils.auth import token_required, role_required

mod_feature_request_api = Blueprint('feature_request', __name__, url_prefix='/api/feature-request')

'''
    Client Adding new feature requests Endpoint - Token is required
'''
@mod_feature_request_api.route('/client/add', methods=['POST'])
@token_required
@role_required('client')
def client_requests(current_user):
    # Get JSON data
    data = request.get_json()

    # Creating new client feature request and setting to this current_user
    client_feature_request = ClientRequest(public_id=str(uuid.uuid4()), subject=data['subject'], description=data['description'], user=current_user)

    # Creating Correspondence for this client request
    correspondence = Correspondence(public_id=str(uuid.uuid4()), client_request=client_feature_request)

    # Executing queries
    db.session.add(client_feature_request)
    db.session.add(correspondence)
    db.session.commit()

    client_request_data = {}
    client_request_data['subject'] = client_feature_request.subject
    client_request_data['description'] = client_feature_request.description
    client_request_data['correspondence'] = correspondence.public_id
    client_request_data['created_date'] = client_feature_request.created_date
    client_request_data['status'] = client_feature_request.status

    return jsonify(client_request_data)

'''
    Get all clients with their feature requests - Token and Admin role is required
'''
@mod_feature_request_api.route('/clients', methods=['GET'])
@token_required
@role_required('admin')
def get_all_client_requests(current_user):

    # Get all client users
    clients = User.query.join(User.role).filter(Role.name.contains('client')).all()

    output = []
    for client in clients:
        user_data = {'feature_requests': []}
        user_data['public_id'] = client.public_id
        user_data['first_name'] = client.first_name
        user_data['last_name'] = client.last_name
        user_data['company'] = client.company
        for client_request in client.client_requests:
            client_request_json = {}
            client_request_json['subject'] = client_request.subject
            client_request_json['description'] = client_request.description
            client_request_json['client_id'] = client_request.client_id
            client_request_json['correspondence'] = client_request.correspondence.public_id
            user_data['feature_requests'].append(client_request_json)
        output.append(user_data)

    return jsonify({'data': output})

'''
    Adding messages to correspondence into feature request
'''
@mod_feature_request_api.route('/add/message/<correspondence_public_id>', methods=['POST'])
@token_required
def send_correspondence_messages_to_feature_request(current_user, correspondence_public_id):
    data = request.get_json()

    # Find the correspondence by public id
    correspondence = Correspondence.query.filter_by(public_id=correspondence_public_id).first()

    # Creating Message and set this correspondence to it
    message = Message(public_id=str(uuid.uuid4()), message=data['message'], correspondence=correspondence, user=current_user)

    db.session.add(message)
    db.session.commit()

    message_json = {}
    message_json['message'] = message.message
    message_json['user_first_name'] = message.user.first_name
    message_json['user_last_name'] = message.user.last_name
    message_json['user_role'] = message.user.role.name
    message_json['correspondence'] = message.correspondence.public_id
    message_json['created_date'] = message.created_date

    return jsonify(message_json)

'''
    Getting all feature request for specific user
'''
@mod_feature_request_api.route('/client', methods=['GET'])
@token_required
def get_client_feature_requests(current_user):
    # Getting all feature requests for this client
    client_feature_requests = ClientRequest.query.filter_by(client_id=current_user.id).all()

    output = []
    for client_feature_request in client_feature_requests:
        client_request_json = {}
        client_request_json['public_id'] = client_feature_request.public_id
        client_request_json['subject'] = client_feature_request.subject
        client_request_json['description'] = client_feature_request.description
        client_request_json['correspondence'] = client_feature_request.correspondence.public_id
        output.append(client_request_json)

    return jsonify({'data': output})

'''
    Getting all messages for specific correspondence of client feature request - Token required
'''
@mod_feature_request_api.route('/messages/<correspondence_public_id>', methods=['GET'])
@token_required
def get_all_messages_by_correspondence(current_user, correspondence_public_id):

    # Get all messages for this correspondence_public_id
    correspondence = Correspondence.query.filter_by(public_id=correspondence_public_id).first()

    correspondence_response = {'correspondence_public_id': correspondence.public_id, 'messages': []}

    for message in correspondence.messages:
        message_json = {}
        message_json['message'] = message.message
        message_json['user_first_name'] = message.user.first_name
        message_json['user_last_name'] = message.user.last_name
        correspondence_response['messages'].append(message_json)

    return jsonify(correspondence_response)

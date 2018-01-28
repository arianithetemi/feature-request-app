import uuid, json, decimal, datetime, jwt
from flask import Blueprint, request, jsonify, make_response
from app.models.user import User
from app.models.role import Role
from app.models.client_request import ClientRequest
from app.models.correspondence import Correspondence
from app import db, bcrypt, secret_key
from app.utils.auth import token_required

mod_feature_request_api = Blueprint('feature_request', __name__, url_prefix='/api/feature-request')

@mod_feature_request_api.route('/client/add/<public_id>', methods=['POST'])
@token_required
def client_requests(current_user, public_id):
    # Get JSON data
    data = request.get_json()

    # query user in db by public_id
    user = User.query.filter_by(public_id=public_id).first()

    # if user not found
    if not user:
        return jsonify({'message': 'No user found!'})

    # Creating new client feature request and setting to this user
    client_feature_request = ClientRequest(subject=data['subject'], description=data['description'], user=user)

    # Creating Correspondence for this client request
    correspondence = Correspondence(public_id=str(uuid.uuid4()), client_request=client_feature_request)

    # Executing queries
    db.session.add(client_feature_request)
    db.session.add(correspondence)
    db.session.commit()

    client_request_data = {}
    client_request_data['subject'] = data['subject']
    client_request_data['description'] = data['description']
    client_request_data['correspondence'] = correspondence.public_id

    return jsonify(client_request_data)

@mod_feature_request_api.route('/clients', methods=['GET'])
@token_required
def get_all_client_requests(current_user):
    users = User.query.join(User.role).filter(Role.name.contains('client')).all()

    output = []
    for user in users:
        user_data = {'feature_requests': []}
        user_data['public_id'] = user.public_id
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        user_data['company'] = user.company
        for client_request in user.client_requests:
            client_request_json = {}
            client_request_json['subject'] = client_request.subject
            client_request_json['description'] = client_request.description
            client_request_json['client_id'] = client_request.client_id
            client_request_json['correspondence'] = client_request.correspondence.public_id
            user_data['feature_requests'].append(client_request_json)
        output.append(user_data)

    return jsonify({'data': output})

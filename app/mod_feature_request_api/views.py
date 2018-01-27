import json, decimal, datetime, jwt
from flask import Blueprint, request, jsonify, make_response
from app.models.user import User
from app.models.role import Role
from app import db, bcrypt, secret_key
from app.utils.auth import token_required

mod_feature_request_api = Blueprint('feature_request', __name__, url_prefix='/api/feature-request')

@mod_feature_request_api.route('/', methods=['GET'])
def client_requests():

    return "hello"

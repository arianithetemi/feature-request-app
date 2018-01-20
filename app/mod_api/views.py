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

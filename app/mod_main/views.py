from flask import Blueprint

mod_main = Blueprint('main', __name__)


@mod_main.route('/', methods=['GET'])
def index():
    ''' Renders the App index page.
    :return:
    '''
    return "Welcome to the Flask App."

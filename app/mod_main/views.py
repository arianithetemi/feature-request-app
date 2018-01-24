from flask import Blueprint, render_template
from app.utils.auth import token_required

mod_main = Blueprint('main', __name__)

@mod_main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@mod_main.route('/dashboard', methods=['GET'])
@token_required
def dashboard(current_user):
    if current_user.role.name == 'client':
        return render_template('client_dashboard.html')
    else:
        return render_template('admin_dashboard.html')

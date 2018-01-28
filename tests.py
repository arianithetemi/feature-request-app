import unittest, json, uuid
from flask_testing import TestCase
from app.models.user import User
from app.models.role import Role
from app import create_app, db, bcrypt

class BaseTestCase(TestCase):

    ############################
    #### setup Flask App and teardown for each test ####
    ############################

    def create_app(self):
        return create_app('testing')

    # executed prior to each test
    def setUp(self):
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()


class UserAPITestCase(BaseTestCase):

    ########################
    #### helper methods ####
    ########################

    def create_client_user(self, first_name, last_name, username, company, email_address, password, confirm_password):
        return self.client.post('/api/user/add', data=json.dumps({'first_name': first_name, 'last_name': last_name, 'username': username, 'company': company,'email_address': email_address,'password': password, 'confirm_password': confirm_password}), content_type='application/json')

    def auth_user(self, username_email, password):
        return self.client.post('/api/auth', data=json.dumps({'username_email': username_email, 'password': password}), content_type='application/json')

    # Testing getting all users without token provided
    def test_get_users_endpoint(self):
        # Making request to endpoint
        response = self.client.get('/api/user/')
        # Decoding JSON response
        data = json.loads(response.data.decode('utf8'))
        # Comparing JSON data
        self.assertEqual(data['message'], "Token is missing")

    def test_create_new_client_user(self):
        response = self.create_client_user('Arianit', 'Hetemi', 'arianit', 'IWS', 'niti@123.com', '123', '123')
        data = json.loads(response.data.decode('utf8'))
        self.assertEqual(data['message'], "Successfully user created!")

    def test_create_new_client_passwords_not_same(self):
        response = self.create_client_user('Arianit', 'Hetemi', 'arianit', 'IWS', 'niti@123.com', '123', '1234')
        data = json.loads(response.data.decode('utf8'))
        self.assertEqual(data['message'], "Password and Confirm Password do not match!")

    def test_login_not_existing_user(self):
        response = self.auth_user('niti', '1234')
        data = json.loads(response.data.decode('utf8'))
        self.assertEqual(data['message'], 'Username or Email is invalid!')

    def test_login_not_activated_client(self):
        username = 'arianit'
        password = 'arianitiniti'

        register_response = self.create_client_user('Arianit', 'Hetemi', username, 'IWS', 'niti@123.com', password, password)

        login_response = self.auth_user(username, password)
        data = json.loads(login_response.data.decode('utf8'))
        self.assertEqual(data['message'], 'Your account is not activated yet!');

    def test_create_admin_test_login(self):
        # Inserting admin into DB
        admin_hash_password = bcrypt.generate_password_hash('toor')

        admin = User(public_id=str(uuid.uuid4()), first_name='John', last_name='Doe', username='johny', company='IWS', active=True, email_address='johny@doe.com', password=admin_hash_password)

        admin_role = Role(name='admin', description="Administrator to manage clients, feature requests and message to clients.", user=admin)

        db.session.add(admin)
        db.session.add(admin_role)
        db.session.commit()

        # Testing admin authentication
        response = self.auth_user(admin.username, 'toor')
        data = json.loads(response.data.decode('utf8'))
        self.assertEqual(data['message'], 'Successfully login')

if __name__ == "__main__":
    unittest.main()

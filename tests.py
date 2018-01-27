import unittest, json
from flask_testing import TestCase
from app import create_app, db

class BaseTestCase(TestCase):

    ############################
    #### setup flask app test and teardown ####
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

        ###############
        #### tests ####
        ###############

class UserAPITestCase(BaseTestCase):

    # Testing getting all users without token provided
    def test_get_users_endpoint(self):
        # Making request to endpoint
        response = self.client.get('/api/user/')
        # Decoding JSON response
        data = json.loads(response.data.decode('utf8'))
        # Comparing JSON data
        self.assertEqual(data['message'], "Token is missing")

if __name__ == "__main__":
    unittest.main()

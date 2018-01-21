import unittest, json
from flask_testing import TestCase
from app import create_app, db

class BaseTestCase(TestCase):

    ############################
    #### setup flask app test and teardown ####
    ############################

    def create_app(self):
        return create_app()

    # executed prior to each test
    def setUp(self):
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == "__main__":
    unittest.main()

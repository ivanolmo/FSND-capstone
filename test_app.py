import unittest
import json

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from .models import setup_db, Player


class BaseballTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'baseball_test'
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'asdf', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_player = {
            'name': 'Kris Bryant',
            'number': 17,
            'position': 'Third Base'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_index(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Cool, it works')


if __name__ == '__main__':
    unittest.main()

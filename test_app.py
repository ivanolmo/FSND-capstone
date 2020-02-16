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

    def test_get_all_players(self):
        res = self.client().get('/players')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['players'])
        self.assertTrue(len(data['players']))

    def test_add_player(self):
        # add a mock player to test add player
        res = self.client().post('/players', json=self.new_player)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_player']['name'], self.new_player['name'])
        self.assertEqual(data['new_player']['number'],
                         self.new_player['number'])
        self.assertEqual(data['new_player']['position'],
                         self.new_player['position'])
        self.assertEqual(data['created_id'], data['new_player']['id'])
        self.assertTrue(data['total_players'])


if __name__ == '__main__':
    unittest.main()

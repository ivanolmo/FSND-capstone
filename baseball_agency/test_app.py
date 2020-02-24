import unittest
import json

from flask_sqlalchemy import SQLAlchemy

from baseball_agency import app
from baseball_agency.models import setup_db, db_drop_and_create_all, Player, \
    Team, Agent


class BaseballTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.database_name = 'baseball_test'
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'asdf', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # mock player, team, and agent to test database functions
        self.test_player = {
            "name": "Test Player Delete",
            "number": "1",
            "position": "Test Position",
            "salary": "Test Salary",
            "team_id": 1,
            "agent_id": 1
        }

        self.test_agent = {
            'name': 'Test Agent Delete'
        }

        self.test_team = {
            'team_name': 'Test Team Delete',
            'team_short': 'TTD',
            'city': 'Test City',
            'state': 'Test State'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass
        # with self.app.app_context():
        #     self.db.session.query(Player).delete()
        #     self.db.session.commit()

    def test_get_index(self):
        response = self.client().get('/')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'index page works')

    def test_get_all_players(self):
        response = self.client().get('/players')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['players'])

    def test_get_player_by_id(self):
        response = self.client().get('/players/2')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['player_details']['id'], 2)
        self.assertTrue(data['total_players'])

    def test_add_player(self):
        # add a mock player to test add_player view
        response = self.client().post('/players', json=self.test_player)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_player']['name'],
                         self.test_player['name'])
        self.assertEqual(data['new_player']['number'],
                         self.test_player['number'])
        self.assertEqual(data['new_player']['position'],
                         self.test_player['position'])
        self.assertEqual(data['new_player']['salary'],
                         self.test_player['salary'])
        self.assertTrue(data['new_player_id'])
        self.assertTrue(data['total_players'])

    def test_delete_player(self):
        # add a mock player to test delete player
        test_delete_player = Player(name='Test', number='0',
                                    position='TestPosition',
                                    salary='1 USD', team_id=1, agent_id=1)
        test_delete_player.insert()
        test_player_id = test_delete_player.id

        response = self.client().delete(f'/players/{test_player_id}')
        data = json.loads(response.data)

        player = Player.query.filter(Player.id == test_player_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], test_player_id)
        self.assertEqual(player, None)
        self.assertTrue(data['total_players'])

    def test_get_all_teams(self):
        response = self.client().get('/teams')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['teams'])

    def test_get_team_by_id(self):
        response = self.client().get('/teams/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['team_details']['id'], 1)
        self.assertEqual(data['team_details']['team_name'], 'Test Team')
        self.assertEqual(data['team_details']['team_short'], 'TTT')
        self.assertEqual(data['team_details']['team_city'], 'Test City')
        self.assertEqual(data['team_details']['team_state'], 'Test State')
        self.assertTrue(data['total_teams'])

    def test_add_team(self):
        # add a mock team to test add_team view
        response = self.client().post('/teams', json=self.test_team)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_team']['team_name'],
                         self.test_team['team_name'])
        self.assertEqual(data['new_team']['team_short'],
                         self.test_team['team_short'])
        self.assertEqual(data['new_team']['team_city'],
                         self.test_team['team_city'])
        self.assertEqual(data['new_team']['team_state'],
                         self.test_team['team_state'])
        self.assertTrue(data['new_team_id'])
        self.assertTrue(data['total_teams'])

    def test_get_all_agents(self):
        response = self.client().get('/agents')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['agents'])

    def test_get_agent_by_id(self):
        response = self.client().get('/agents/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['agent']['name'], 'Test Agent')
        self.assertEqual(data['agent']['id'], 1)

    def test_add_agent(self):
        response = self.client().post('/agents', json=self.test_agent)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_agent']['name'], self.test_agent['name'])
        self.assertTrue(data['new_agent_id'])
        self.assertTrue(len(data['agents']))
        self.assertTrue(data['total_agents'])

    def test_delete_agent(self):
        test_agent = Agent(name='Test Agent')
        test_agent.insert()
        test_agent_id = test_agent.id

        response = self.client().delete(f'/agents/{test_agent_id}')
        data = json.loads(response.data)

        agent = Agent.query.filter(Agent.id == test_agent_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], test_agent_id)
        self.assertEqual(agent, None)
        self.assertTrue(data['total_agents'])


if __name__ == '__main__':
    unittest.main()

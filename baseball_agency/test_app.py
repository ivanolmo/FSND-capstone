import unittest
import json

from flask_sqlalchemy import SQLAlchemy

from baseball_agency import app
from baseball_agency.models import db, setup_db, db_drop_and_create_all, \
    Player, Team, Agent


class BaseballTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.database_name = 'baseball_test'
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'asdf', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        db.session.close()
        db_drop_and_create_all()

        self.mock_player = Player(name='Test Name', number='00',
                                  position='Test Position',
                                  salary='Test Salary', team_id=1,
                                  agent_id=1)

        # mock team and agent to test database functions
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.test_agent = Agent(
                name="Test Agent"
            )
            self.test_team = Team(
                team_name="Test Team",
                team_short="TTT",
                team_city="Test City",
                team_state="Test State"
            )
            self.test_agent.insert()
            self.test_team.insert()

    def tearDown(self):
        pass

    def test_get_index(self):
        response = self.client().get('/')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'index page works')

    def test_get_all_players(self):
        # add one player because db starts with empty player table
        self.mock_player.insert()

        response = self.client().get('/players')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['players']),
        self.assertEqual(data['total_players'], 1)

    def test_get_player_by_id(self):
        self.mock_player.insert()
        mock_player_id = self.mock_player.id

        response = self.client().get(f'/players/{mock_player_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['player_details']['id'], mock_player_id)
        self.assertTrue(data['total_players'])

    def test_post_add_player(self):
        # add a mock player to test add_player view
        test_player = {
            "name": "New Test Player",
            "number": "99",
            "position": "New Test Position",
            "salary": "New Test Salary",
            "team_id": 1,
            "agent_id": 1
        }

        response = self.client().post('/players', json=test_player)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_player']['name'],
                         test_player['name'])
        self.assertEqual(data['new_player']['number'],
                         test_player['number'])
        self.assertEqual(data['new_player']['position'],
                         test_player['position'])
        self.assertEqual(data['new_player']['salary'],
                         test_player['salary'])
        self.assertTrue(data['new_player_id'])
        self.assertTrue(data['total_players'])

    def test_delete_player(self):
        # add a mock player to test delete player
        self.mock_player.insert()
        test_player_id = self.mock_player.id

        self.assertEqual(len(Player.query.all()), 1)

        response = self.client().delete(f'/players/{test_player_id}')
        data = json.loads(response.data)

        player = Player.query.filter(Player.id == test_player_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], test_player_id)
        self.assertEqual(player, None)
        self.assertEqual(data['total_players'], 0)

    def test_patch_player(self):
        # insert mock player to edit
        self.mock_player.insert()
        test_player_to_edit_id = self.mock_player.id

        test_edit_body = {
            'name': 'After Player Edit',
            'number': '99',
            'position': 'AfterPlayerEdit',
            'salary': '999 million USD'
        }

        response = self.client().patch(f'/players/{test_player_to_edit_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_player'])
        self.assertEqual(data['updated_player']['name'], test_edit_body[
            'name'])
        self.assertEqual(data['updated_player']['number'], test_edit_body[
            'number'])
        self.assertEqual(data['updated_player']['position'], test_edit_body[
            'position'])
        self.assertEqual(data['updated_player']['salary'], test_edit_body[
            'salary'])

    def test_get_all_teams(self):
        response = self.client().get('/teams')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['teams'])
        self.assertEqual(data['total_teams'], 1)

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

    def test_get_team_players(self):
        # add one player to team with team_id of 1 so query returns something
        self.mock_player.insert()

        response = self.client().get('/teams/1/players')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['roster'])
        self.assertEqual(data['total_team_players'], 1)

    def test_post_team(self):
        # add a mock team to test post_team view
        test_team = {
            "team_name": "New Test Team",
            "team_short": "TEST",
            "team_city": "New Test City",
            "team_state": "New Test State"
        }
        response = self.client().post('/teams', json=test_team)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_team']['team_name'],
                         test_team['team_name'])
        self.assertEqual(data['new_team']['team_short'],
                         test_team['team_short'])
        self.assertEqual(data['new_team']['team_city'],
                         test_team['team_city'])
        self.assertEqual(data['new_team']['team_state'],
                         test_team['team_state'])
        self.assertTrue(data['new_team_id'])
        self.assertTrue(data['total_teams'])

    def test_delete_team(self):
        # query mock team previously loaded into db
        test_team_to_delete = Team.query.first_or_404()
        delete_id = test_team_to_delete.id

        self.assertEqual(len(Team.query.all()), 1)

        response = self.client().delete(f'/teams/{delete_id}')
        data = json.loads(response.data)

        team = Team.query.filter(Team.id == delete_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], delete_id)
        self.assertEqual(team, None)
        self.assertEqual(data['total_teams'], 0)

    def test_patch_team(self):
        # query existing mock team to edit
        test_team_to_edit = Team.query.filter_by(id=1).one_or_none()
        test_team_to_edit_id = test_team_to_edit.id

        test_edit_body = {
            'team_name': 'After Team Edit',
            'team_short': 'EDIT',
            'team_city': 'AfterEdit City',
            'team_state': 'AfterEdit State'
        }

        response = self.client().patch(f'/teams/{test_team_to_edit_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_team'])
        self.assertEqual(data['updated_team']['team_name'], test_edit_body[
            'team_name'])
        self.assertEqual(data['updated_team']['team_short'], test_edit_body[
            'team_short'])
        self.assertEqual(data['updated_team']['team_city'], test_edit_body[
            'team_city'])
        self.assertEqual(data['updated_team']['team_state'], test_edit_body[
            'team_state'])

    def test_get_all_agents(self):
        response = self.client().get('/agents')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['agents'])
        self.assertEqual(data['total_agents'], 1)

    def test_get_agent_by_id(self):
        response = self.client().get('/agents/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['agent']['name'], 'Test Agent')
        self.assertEqual(data['agent']['id'], 1)

    def test_get_agent_clients(self):
        # add one player to agent with agent_id of 1 so query returns something
        self.mock_player.insert()
        agent = Agent.query.filter_by(id=1).one_or_none()

        response = self.client().get('/agents/1/clients')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['clients'])
        self.assertEqual(data['total_agent_clients'], 1)
        self.assertEqual(data['agent_name'], agent.name)

    def test_post_agent(self):
        # add a mock agent to test post_agent view
        test_agent = {
            "name": "New Test Agent"
        }
        response = self.client().post('/agents', json=test_agent)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_agent']['name'], test_agent['name'])
        self.assertTrue(data['new_agent_id'])
        self.assertTrue(len(data['agents']))
        self.assertTrue(data['total_agents'])

    def test_delete_agent(self):
        # query mock agent previously loaded into db
        test_agent_to_delete = Agent.query.first_or_404()
        delete_id = test_agent_to_delete.id

        self.assertEqual(len(Agent.query.all()), 1)

        response = self.client().delete(f'/agents/{delete_id}')
        data = json.loads(response.data)

        agent = Agent.query.filter(Agent.id == delete_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], delete_id)
        self.assertEqual(agent, None)
        self.assertEqual(data['total_agents'], 0)

    def test_patch_agent(self):
        # query existing mock agent to edit
        test_agent_to_edit = Agent.query.filter_by(id=1).one_or_none()
        test_agent_to_edit_id = test_agent_to_edit.id

        test_edit_body = {
            'name': 'After Agent Edit'
        }

        response = self.client().patch(f'/agents/{test_agent_to_edit_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_agent'])
        self.assertEqual(data['updated_agent']['name'], test_edit_body['name'])


if __name__ == '__main__':
    unittest.main()

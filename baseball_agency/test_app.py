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
        self.database_path = 'postgres://{}:{}@{}/{}'.format(
            'postgres', 'asdf', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        db.session.close()
        db_drop_and_create_all()

        # create mock player, team, and agent to insert as needed
        self.mock_player = Player(
            name='Test Player',
            number='00',
            position='Test Position',
            salary='Test Salary USD',
            team_id=1,
            agent_id=1
        )
        self.mock_agent = Agent(
            name='Test Agent',
            salary='Test Salary USD'
        )
        self.mock_team = Team(
            name='Test Team',
            abbr='TTT',
            city='Test City',
            state='Test State',
            total_payroll='Test Salary USD'
        )

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        pass

    def test_get_index(self):
        response = self.client().get('/')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'index page works')

    """
    Player Tests
    """

    def test_get_all_players(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # insert a mock player to test post_player view
        self.mock_player.insert()

        response = self.client().get('/players')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['players']),
        self.assertEqual(data['total_players'], 1)

    def test_get_all_players_empty_database(self):
        response = self.client().get('/players')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found '
                                          'on the server. If you entered the '
                                          'URL manually please check your '
                                          'spelling and try again.')

    def test_get_player_by_id(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # insert a mock player to test post_player view
        self.mock_player.insert()

        mock_player_id = self.mock_player.id

        response = self.client().get(f'/players/{mock_player_id}/details')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['player_details']['id'], mock_player_id)

    def test_get_player_by_id_not_exist(self):
        response = self.client().get('/players/9000/details')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found '
                                          'on the server. If you entered the '
                                          'URL manually please check your '
                                          'spelling and try again.')

    def test_post_player(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # mock player to test post_player view
        test_player = {
            'name': 'New Test Player',
            'number': '99',
            'position': 'New Test Position',
            'salary': 'New Test Salary',
            'team_id': 1,
            'agent_id': 1
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

    def test_post_player_invalid_agent_id_not_exist(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # mock player to test post_player view
        test_player = {
            'name': 'New Test Player',
            'number': '99',
            'position': 'New Test Position',
            'salary': 'New Test Salary',
            'team_id': 1,
            'agent_id': 9000
        }

        response = self.client().post('/players', json=test_player)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_player_invalid_agent_id_not_integer(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # mock player to test post_player view
        test_player = {
            'name': 'New Test Player',
            'number': '99',
            'position': 'New Test Position',
            'salary': 'New Test Salary',
            'team_id': 1,
            'agent_id': '1'
        }

        response = self.client().post('/players', json=test_player)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_player_invalid_team_id_not_exist(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # mock player to test post_player view
        test_player = {
            'name': 'New Test Player',
            'number': '99',
            'position': 'New Test Position',
            'salary': 'New Test Salary',
            'team_id': 9000,
            'agent_id': 1
        }

        response = self.client().post('/players', json=test_player)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_player_invalid_team_id_not_integer(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # mock player to test post_player view
        test_player = {
            'name': 'New Test Player',
            'number': '99',
            'position': 'New Test Position',
            'salary': 'New Test Salary',
            'team_id': '1',
            'agent_id': 1
        }

        response = self.client().post('/players', json=test_player)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_player_invalid_body_spelling(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # mock player to test post_player view
        test_player = {
            'namme': 'Test Name',
            'nummmer': '99',
            'possition': 'New Test Position',
            'saary': 'New Test Salary',
            'eam_id': 1,
            'agnt_id': 1
        }

        response = self.client().post('/players', json=test_player)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_player_invalid_body_missing_name(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # mock player to test post_player view
        test_player = {
            'number': '99',
            'position': 'New Test Position',
            'salary': 'New Test Salary',
            'team_id': 1,
            'agent_id': 1
        }

        response = self.client().post('/players', json=test_player)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_player_invalid_body_missing_number(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # mock player to test post_player view
        test_player = {
            'name': 'New Test Player',
            'position': 'New Test Position',
            'salary': 'New Test Salary',
            'team_id': 1,
            'agent_id': 1
        }

        response = self.client().post('/players', json=test_player)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_player_invalid_body_missing_position(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # mock player to test post_player view
        test_player = {
            'name': 'New Test Player',
            'number': '99',
            'salary': 'New Test Salary',
            'team_id': 1,
            'agent_id': 1
        }

        response = self.client().post('/players', json=test_player)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_player_invalid_body_missing_salary(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # mock player to test post_player view
        test_player = {
            'name': 'New Test Player',
            'number': '99',
            'position': 'New Test Position',
            'team_id': 1,
            'agent_id': 1
        }

        response = self.client().post('/players', json=test_player)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_player_invalid_body_missing_team_id(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # mock player to test post_player view
        test_player = {
            'name': 'New Test Player',
            'number': '99',
            'position': 'New Test Position',
            'salary': 'New Test Salary',
            'agent_id': 1
        }

        response = self.client().post('/players', json=test_player)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_player_invalid_body_missing_agent_id(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # mock player to test post_player view
        test_player = {
            'name': 'New Test Player',
            'number': '99',
            'position': 'New Test Position',
            'salary': 'New Test Salary',
            'team_id': 1
        }

        response = self.client().post('/players', json=test_player)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_delete_player(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # insert a mock player to test delete player
        self.mock_player.insert()
        mock_player_id = self.mock_player.id

        self.assertEqual(len(Player.query.all()), 1)

        response = self.client().delete(f'/players/{mock_player_id}')
        data = json.loads(response.data)

        player = Player.query.filter(Player.id == mock_player_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], mock_player_id)
        self.assertEqual(player, None)
        self.assertEqual(data['total_players'], 0)

    def test_delete_player_not_exist(self):
        response = self.client().delete('/players/9000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found '
                                          'on the server. If you entered the '
                                          'URL manually please check your '
                                          'spelling and try again.')

    def test_patch_player(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # insert a mock player to patch
        self.mock_player.insert()

        mock_player_id = self.mock_player.id

        test_edit_body = {
            'name': 'After Player Edit',
            'number': '99',
            'position': 'AfterPlayerEdit',
            'salary': '999 million USD'
        }

        response = self.client().patch(f'/players/{mock_player_id}',
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

    def test_patch_player_not_exist(self):
        response = self.client().patch('/players/9000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found '
                                          'on the server. If you entered the '
                                          'URL manually please check your '
                                          'spelling and try again.')

    def test_patch_player_invalid_agent_id(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # insert a mock player to patch
        self.mock_player.insert()

        mock_player_id = self.mock_player.id

        test_edit_body = {
            'agent_id': 9000
        }

        response = self.client().patch(f'/players/{mock_player_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The team_id or agent_id you '
                                          'entered does not exist in the '
                                          'database. Please check your input '
                                          'and try again.')

    def test_patch_player_invalid_team_id(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # insert a mock player to patch
        self.mock_player.insert()

        mock_player_id = self.mock_player.id

        test_edit_body = {
            'team_id': 9000
        }

        response = self.client().patch(f'/players/{mock_player_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The team_id or agent_id you '
                                          'entered does not exist in the '
                                          'database. Please check your input '
                                          'and try again.')

    def test_patch_player_invalid_body_empty_name(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # insert a mock player to patch
        self.mock_player.insert()

        mock_player_id = self.mock_player.id

        test_edit_body = {
            'name': ''
        }

        response = self.client().patch(f'/players/{mock_player_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_patch_player_invalid_body_empty_number(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # insert a mock player to patch
        self.mock_player.insert()

        mock_player_id = self.mock_player.id

        test_edit_body = {
            'number': ''
        }

        response = self.client().patch(f'/players/{mock_player_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_patch_player_invalid_body_empty_position(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # insert a mock player to patch
        self.mock_player.insert()

        mock_player_id = self.mock_player.id

        test_edit_body = {
            'position': ''
        }

        response = self.client().patch(f'/players/{mock_player_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_patch_player_invalid_body_empty_salary(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # insert a mock player to patch
        self.mock_player.insert()

        mock_player_id = self.mock_player.id

        test_edit_body = {
            'salary': ''
        }

        response = self.client().patch(f'/players/{mock_player_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    """
    Team Tests
    """

    def test_get_all_teams(self):
        # insert mock team because db initializes empty
        self.mock_team.insert()

        response = self.client().get('/teams')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['teams'])
        self.assertEqual(data['total_teams'], 1)

    def test_get_all_teams_emtpy_database(self):
        response = self.client().get('/teams')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found '
                                          'on the server. If you entered the '
                                          'URL manually please check your '
                                          'spelling and try again.')

    def test_get_team_by_id(self):
        # insert mock team because db initializes empty
        self.mock_team.insert()

        mock_team_id = self.mock_team.id

        response = self.client().get(f'/teams/{mock_team_id}/details')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['team_details']['id'], 1)
        self.assertEqual(data['team_details']['name'], 'Test Team')
        self.assertEqual(data['team_details']['abbr'], 'TTT')
        self.assertEqual(data['team_details']['city'], 'Test City')
        self.assertEqual(data['team_details']['state'], 'Test State')
        self.assertEqual(data['team_details']['total_payroll'],
                         'Test Salary USD')

    def test_get_team_by_id_not_exist(self):
        response = self.client().get('/teams/9000/details')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found '
                                          'on the server. If you entered the '
                                          'URL manually please check your '
                                          'spelling and try again.')

    def test_get_team_players(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        mock_team_id = self.mock_team.id

        # insert one player to team with team_id of 1 so query returns
        # something
        self.mock_player.insert()

        response = self.client().get(f'/teams/{mock_team_id}/players')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['roster'])
        self.assertEqual(data['total_team_players'], 1)

    def test_get_team_players_empty_roster(self):
        # insert mock team because db initializes empty
        self.mock_team.insert()
        mock_team_id = self.mock_team.id

        response = self.client().get(f'/teams/{mock_team_id}/players')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_team_players'], 0)
        self.assertFalse(data['roster'])

    def test_get_team_players_team_not_exist(self):
        response = self.client().get('/teams/9000/players')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found '
                                          'on the server. If you entered the '
                                          'URL manually please check your '
                                          'spelling and try again.')

    def test_post_team(self):
        # add a mock team to test post_team view
        mock_team = {
            'name': 'New Test Team',
            'abbr': 'TEST',
            'city': 'New Test City',
            'state': 'New Test State',
            'total_payroll': '1 million USD'
        }

        response = self.client().post('/teams', json=mock_team)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_team']['name'],
                         mock_team['name'])
        self.assertEqual(data['new_team']['abbr'],
                         mock_team['abbr'])
        self.assertEqual(data['new_team']['city'],
                         mock_team['city'])
        self.assertEqual(data['new_team']['state'],
                         mock_team['state'])
        self.assertEqual(data['new_team']['total_payroll'],
                         mock_team['total_payroll'])
        self.assertTrue(data['new_team_id'])
        self.assertTrue(data['total_teams'])

    def test_post_team_invalid_body_spelling(self):
        # add a mock team to test post_team view
        mock_team = {
            'tear_name': 'New Test Team',
            'abbrt': 'TEST',
            'team_ciddy': 'New Test City',
            'tam_state': 'New Test State',
            'ttl_paryoll': '1 million USD'
        }

        response = self.client().post('/teams', json=mock_team)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_team_invalid_body_missing_name(self):
        # add a mock team to test post_team view
        mock_team = {
            'abbr': 'TEST',
            'city': 'New Test City',
            'state': 'New Test State'
        }

        response = self.client().post('/teams', json=mock_team)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_team_invalid_body_missing_abbr(self):
        # add a mock team to test post_team view
        mock_team = {
            'name': 'New Test Team',
            'city': 'New Test City',
            'state': 'New Test State'
        }

        response = self.client().post('/teams', json=mock_team)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_team_invalid_body_missing_city(self):
        # add a mock team to test post_team view
        mock_team = {
            'name': 'New Test Team',
            'abbr': 'TEST',
            'state': 'New Test State'
        }

        response = self.client().post('/teams', json=mock_team)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_team_invalid_body_missing_state(self):
        # add a mock team to test post_team view
        mock_team = {
            'name': 'New Test Team',
            'abbr': 'TEST',
            'city': 'New Test City'
        }

        response = self.client().post('/teams', json=mock_team)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_team_invalid_body_missing_total_payroll(self):
        # add a mock team to test post_team view
        mock_team = {
            'name': 'New Test Team',
            'abbr': 'TEST',
            'city': 'New Test City',
            'state': 'New Test State'
        }

        response = self.client().post('/teams', json=mock_team)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_delete_team(self):
        # insert mock team because db initializes empty
        self.mock_team.insert()

        mock_team_id = self.mock_team.id

        self.assertEqual(len(Team.query.all()), 1)

        response = self.client().delete(f'/teams/{mock_team_id}')
        data = json.loads(response.data)

        team = Team.query.filter(Team.id == mock_team_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], mock_team_id)
        self.assertEqual(team, None)
        self.assertEqual(data['total_teams'], 0)

    def test_delete_team_not_exist(self):
        response = self.client().delete('/teams/9000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found '
                                          'on the server. If you entered the '
                                          'URL manually please check your '
                                          'spelling and try again.')

    def test_patch_team(self):
        # insert mock team because db initializes empty
        self.mock_team.insert()
        mock_team_id = self.mock_team.id

        test_edit_body = {
            'name': 'After Team Edit',
            'abbr': 'EDIT',
            'city': 'AfterEdit City',
            'state': 'AfterEdit State',
            'total_payroll': 'AfterEdit USD'
        }

        response = self.client().patch(f'/teams/{mock_team_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_team'])
        self.assertEqual(data['updated_team']['name'], test_edit_body[
            'name'])
        self.assertEqual(data['updated_team']['abbr'], test_edit_body[
            'abbr'])
        self.assertEqual(data['updated_team']['city'], test_edit_body[
            'city'])
        self.assertEqual(data['updated_team']['state'], test_edit_body[
            'state'])
        self.assertEqual(data['updated_team']['total_payroll'],
                         test_edit_body['total_payroll'])

    def test_patch_team_not_exist(self):
        response = self.client().patch('/teams/9000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found '
                                          'on the server. If you entered the '
                                          'URL manually please check your '
                                          'spelling and try again.')

    def test_patch_team_invalid_body_spelling(self):
        # insert mock team because db initializes empty
        self.mock_team.insert()

        mock_team_id = self.mock_team.id

        test_edit_body = {
            'tear_name': 'New Test Team',
            'abbrt': 'TEST',
            'team_ciddy': 'New Test City',
            'tam_state': 'New Test State',
            'tolta_pryaoll': '1 million USD'
        }

        response = self.client().patch(f'/teams/{mock_team_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_patch_team_invalid_body_empty_name(self):
        # insert mock team because db initializes empty
        self.mock_team.insert()

        mock_team_id = self.mock_team.id

        test_edit_body = {
            'name': ''
        }

        response = self.client().patch(f'/teams/{mock_team_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_patch_team_invalid_body_empty_abbr(self):
        # insert mock team because db initializes empty
        self.mock_team.insert()

        mock_team_id = self.mock_team.id

        test_edit_body = {
            'abbr': ''
        }

        response = self.client().patch(f'/teams/{mock_team_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_patch_player_invalid_body_empty_city(self):
        # insert mock team because db initializes empty
        self.mock_team.insert()

        mock_team_id = self.mock_team.id

        test_edit_body = {
            'city': ''
        }

        response = self.client().patch(f'/teams/{mock_team_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_patch_player_invalid_body_empty_state(self):
        # insert mock team because db initializes empty
        self.mock_team.insert()

        mock_team_id = self.mock_team.id

        test_edit_body = {
            'state': ''
        }

        response = self.client().patch(f'/teams/{mock_team_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_patch_player_invalid_body_empty_total_payroll(self):
        # insert mock team because db initializes empty
        self.mock_team.insert()

        mock_team_id = self.mock_team.id

        test_edit_body = {
            'total_payroll': ''
        }

        response = self.client().patch(f'/teams/{mock_team_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    """
    Agent Tests
    """

    def test_get_all_agents(self):
        # insert mock agent because db initializes empty
        self.mock_agent.insert()

        response = self.client().get('/agents')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['agents'])
        self.assertEqual(data['total_agents'], 1)

    def test_get_all_agents_empty_database(self):
        response = self.client().get('/agents')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found '
                                          'on the server. If you entered the '
                                          'URL manually please check your '
                                          'spelling and try again.')

    def test_get_agent_by_id(self):
        # insert mock agent because db initializes empty
        self.mock_agent.insert()

        mock_agent_id = self.mock_agent.id

        response = self.client().get(f'/agents/{mock_agent_id}/details')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['agent']['id'], 1)
        self.assertEqual(data['agent']['name'], 'Test Agent')
        self.assertEqual(data['agent']['salary'], 'Test Salary USD')

    def test_get_agent_by_id_not_exist(self):
        response = self.client().get('/agents/9000/details')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found '
                                          'on the server. If you entered the '
                                          'URL manually please check your '
                                          'spelling and try again.')

    def test_get_agent_clients(self):
        # posting a player requires pre-existing team and agent in db
        self.mock_agent.insert()
        self.mock_team.insert()

        # insert one player to agent using agent_id of 1 so query returns
        # something
        self.mock_player.insert()

        mock_agent_id = self.mock_agent.id

        response = self.client().get(f'/agents/{mock_agent_id}/clients')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['clients'])
        self.assertEqual(data['total_agent_clients'], 1)
        self.assertEqual(data['agent'], self.mock_agent.name)

    def test_get_agent_clients_agent_not_exist(self):
        response = self.client().get('/agents/9000/players')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found '
                                          'on the server. If you entered the '
                                          'URL manually please check your '
                                          'spelling and try again.')

    def test_post_agent(self):
        # mock agent to test post_agent view
        mock_agent = {
            'name': 'New Test Agent',
            'salary': '1 million USD'
        }

        response = self.client().post('/agents', json=mock_agent)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_agent']['name'], mock_agent['name'])
        self.assertEqual(data['new_agent']['salary'], mock_agent['salary'])
        self.assertTrue(data['new_agent_id'])
        self.assertTrue(data['total_agents'])

    def test_post_agent_invalid_body_spelling(self):
        mock_agent = {
            'naaame': 'New Test Agent',
            'slaray': '1 million USD'
        }

        response = self.client().post('/agents', json=mock_agent)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_agent_invalid_body_empty_name(self):
        mock_agent = {
            'salary': '1 million USD'
        }

        response = self.client().post('/agents', json=mock_agent)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_post_agent_invalid_body_empty_salary(self):
        mock_agent = {
            'name': 'Test Agent'
        }

        response = self.client().post('/agents', json=mock_agent)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_delete_agent(self):
        # insert mock agent because db initializes empty
        self.mock_agent.insert()

        mock_agent_id = self.mock_agent.id

        self.assertEqual(len(Agent.query.all()), 1)

        response = self.client().delete(f'/agents/{mock_agent_id}')
        data = json.loads(response.data)

        agent = Agent.query.filter(Agent.id == mock_agent_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(Agent.query.all()), 0)
        self.assertEqual(data['deleted_id'], mock_agent_id)
        self.assertEqual(agent, None)
        self.assertEqual(data['total_agents'], 0)

    def test_delete_agent_not_exist(self):
        response = self.client().delete('/agents/9000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found '
                                          'on the server. If you entered the '
                                          'URL manually please check your '
                                          'spelling and try again.')

    def test_patch_agent(self):
        # insert mock agent because db initializes empty
        self.mock_agent.insert()

        mock_agent_id = self.mock_agent.id

        test_edit_body = {
            'name': 'After Agent Edit',
            'salary': 'After Salary Edit'
        }

        response = self.client().patch(f'/agents/{mock_agent_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_agent'])
        self.assertEqual(data['updated_agent']['name'], test_edit_body['name'])
        self.assertEqual(data['updated_agent']['salary'], test_edit_body[
            'salary'])

    def test_patch_agent_not_exist(self):
        response = self.client().patch('/agents/9000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested URL was not found '
                                          'on the server. If you entered the '
                                          'URL manually please check your '
                                          'spelling and try again.')

    def test_patch_agent_invalid_body_empty_name(self):
        # insert mock agent because db initializes empty
        self.mock_agent.insert()

        mock_agent_id = self.mock_agent.id

        test_edit_body = {
            'name': ''
        }

        response = self.client().patch(f'/agents/{mock_agent_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_patch_agent_invalid_body_empty_salary(self):
        # insert mock agent because db initializes empty
        self.mock_agent.insert()

        mock_agent_id = self.mock_agent.id

        test_edit_body = {
            'salary': ''
        }

        response = self.client().patch(f'/agents/{mock_agent_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')

    def test_patch_agent_invalid_body_spelling(self):
        # insert mock agent because db initializes empty
        self.mock_agent.insert()

        mock_agent_id = self.mock_agent.id

        test_edit_body = {
            'nanmame': 'New Test Agent'
        }

        response = self.client().patch(f'/agents/{mock_agent_id}',
                                       json=test_edit_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'The browser (or proxy) sent a '
                                          'request that this server could '
                                          'not understand.')


if __name__ == '__main__':
    unittest.main()

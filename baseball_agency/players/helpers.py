from sqlalchemy.exc import IntegrityError

from ..models import Agent, Team


def check_valid_agent_id(id):
    is_valid = True
    valid_agent_ids = [agent.id for agent in Agent.query.all()]

    if not id in valid_agent_ids:
        is_valid = False

    return is_valid


def check_valid_team_id(id):
    is_valid = True
    valid_team_ids = [team.id for team in Team.query.all()]

    if not id in valid_team_ids:
        is_valid = False

    return is_valid


def valid_player_body(body):
    is_valid = True

    string_keys = [
        'name', 'position', 'salary', 'number'
    ]

    integer_keys = [
        'agent_id', 'team_id'
    ]

    try:
        for key in string_keys:
            if key not in body.keys() or body[key] == '':
                is_valid = False

        for key in integer_keys:
            if key not in body.keys() or body[key] == 0:
                is_valid = False

        if not check_valid_agent_id(body['agent_id']):
            is_valid = False

        if not check_valid_team_id(body['team_id']):
            is_valid = False

    except ValueError:
        is_valid = False
    except KeyError:
        is_valid = False
    except Exception:
        raise Exception

    return is_valid


def valid_player_patch_body(body):
    # separate function to check patch body
    is_valid = True

    possible_keys = [
        'name', 'number', 'position', 'salary', 'team_id', 'agent_id'
    ]

    if body is None:
        is_valid = False

    for key in body.keys():
        if key not in possible_keys or body[key] == '':
            is_valid = False

    if 'team_id' in body:
        if not check_valid_team_id(body['team_id']):
            return IntegrityError

    if 'agent_id' in body:
        if not check_valid_agent_id(body['agent_id']):
            return IntegrityError

    return is_valid

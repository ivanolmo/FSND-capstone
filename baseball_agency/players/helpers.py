from ..models import Agent, Team


def valid_player_body(body):
    is_valid = True

    string_keys = [
        'name', 'position', 'salary', 'number'
    ]

    integer_keys = [
        'agent_id', 'team_id'
    ]

    valid_agent_ids = [agent.id for agent in Agent.query.all()]
    valid_team_ids = [team.id for team in Team.query.all()]

    try:
        if int(body['number']) != type(int):
            raise ValueError

        for key in string_keys:
            if key not in body.keys() or body[key] == '':
                is_valid = False

        for key in integer_keys:
            if key not in body.keys() or body[key] == 0:
                is_valid = False

        if body['agent_id'] not in valid_agent_ids:
            is_valid = False

        if body['team_id'] not in valid_team_ids:
            is_valid = False

    except ValueError:
        is_valid = False
    except KeyError:
        is_valid = False
    except Exception:
        raise Exception

    return is_valid

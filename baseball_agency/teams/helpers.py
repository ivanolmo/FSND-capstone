def valid_team_body(body):
    is_valid = True

    expected_key = ['team_name', 'team_short', 'team_city', 'team_state']

    try:
        for key in expected_key:
            if key not in body.keys() or body[key] == '':
                is_valid = False

    except ValueError:
        is_valid = False
    except KeyError:
        is_valid = False
    except Exception:
        raise Exception

    return is_valid

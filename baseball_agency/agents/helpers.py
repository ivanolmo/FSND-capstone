def valid_agent_body(body):
    is_valid = True

    expected_key = ['name']

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

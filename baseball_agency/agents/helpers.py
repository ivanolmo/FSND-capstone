def valid_agent_body(body):
    is_valid = True

    expected_keys = [
        'name', 'salary'
    ]

    try:
        for key in expected_keys:
            if key not in body.keys() or body[key] == '':
                is_valid = False

    except ValueError:
        is_valid = False
    except KeyError:
        is_valid = False
    except Exception:
        raise Exception

    return is_valid


def valid_agent_patch_body(body):
    is_valid = True

    possible_keys = [
        'name', 'salary'
    ]

    if body is None:
        is_valid = False

    for key in body.keys():
        if key not in possible_keys or body[key] == '':
            is_valid = False

    return is_valid

from flask_cors import CORS
from flask import Flask, request, jsonify, abort

from baseball_agency.models import Player, setup_db

# from auth.auth import requires_auth

# db_drop_and_create_all()

PLAYERS_PER_PAGE = 10


# def create_app(test_config=None):
app = Flask(__name__)
setup_db(app)
CORS(app, resource={r'/api/*': {'origins': '*'}})


def paginate_players(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * PLAYERS_PER_PAGE
    end = start + PLAYERS_PER_PAGE

    players = [player.format() for player in selection]
    current_players = players[start:end]

    return current_players


# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Headers',
#                          'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods',
#                          'GET,POST,PATCH,DELETE,OPTIONS')
#     return response


@app.route('/', methods=['GET'])
def index():
    # placeholder test endpoint
    return jsonify({
        'success': True,
        'message': 'Cool, it works'
    }), 200


@app.route('/players', methods=['GET'])
def get_players():
    # requires no authentication
    try:
        players = Player.query.all()

        if not players:
            abort(404)

        players = [player.format() for player in players]

        return jsonify({
            'success': True,
            'players': players
        }), 200

    except Exception as error:
        raise error


@app.route('/players', methods=['POST'])
def add_player():
    # will require authentication
    try:
        body = request.get_json()
        name = body.get('name', None)
        number = body.get('number', None)
        position = body.get('position', None)

        if name is None or number is None or position is None:
            abort(400)
        if len(name) == 0 or len(position) == 0 or not isinstance(
                number, int):
            abort(400)

        new_player = Player(name=name, number=number, position=position)
        new_player.insert()

        current_players = paginate_players(request,
                                           Player.query.order_by(
                                               Player.id).all())

        return jsonify({
            'success': True,
            'created_id': new_player.id,
            'new_player': new_player.format(),
            'players': current_players,
            'total_players': len(Player.query.all())
        }), 201

    except Exception as error:
        raise error


@app.route('/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    # will require authentication
    try:
        player = Player.query.filter(Player.id == player_id).one_or_none()
        if player is None:
            abort(404)
        player.delete()

        return jsonify({
            'success': True,
            'deleted_id': player.id,
            'total_players': len(Player.query.all())
        })

    except Exception as error:
        raise error

    # return app


# if __name__ == '__main__':
#     create_app()

from flask_cors import CORS
from flask import Flask, request, jsonify, abort

from models import Player, Stats, setup_db, db_drop_and_create_all

# from auth.auth import requires_auth

# db_drop_and_create_all()

PLAYERS_PER_PAGE = 10


def paginate_players(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * PLAYERS_PER_PAGE
    end = start + PLAYERS_PER_PAGE

    players = [player.format() for player in selection]
    current_players = players[start:end]

    return current_players


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resource={r'/api/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,DELETE,OPTIONS')
        return response

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

    return app


if __name__ == '__main__':
    create_app()

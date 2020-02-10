from flask_cors import CORS
from flask import Flask, request, jsonify, abort

from models import Player, PlayerDetails, PlayerStats, TeamStats, setup_db, \
    db_drop_and_create_all

from auth.auth import requires_auth

# db_drop_and_create_all()

app = Flask(__name__)
setup_db(app)
CORS(app)

"""
API endpoints
"""


@app.route('/', methods=['GET'])
def index():
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


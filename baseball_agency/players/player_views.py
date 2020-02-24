import json

from flask import Blueprint, jsonify, request, abort

from .. import app
from ..models import Player, Agent, Team
from .helpers import valid_player_body

players = Blueprint('players', __name__)

PLAYERS_PER_PAGE = 10


def paginate_players(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * PLAYERS_PER_PAGE
    end = start + PLAYERS_PER_PAGE

    players = [player.format() for player in selection]
    current_players = players[start:end]

    return current_players


@players.route('/players', methods=['GET'])
def get_players():
    # requires no authentication, public
    try:
        player_query = Player.query.all()

        if not player_query:
            abort(404)

        players = [player.format() for player in player_query]

        return jsonify({
            'success': True,
            'players': players
        }), 200

    except Exception as error:
        raise error


@players.route('/players/<int:player_id>', methods=['GET'])
def get_specific_player_details(player_id):
    # will require authentication level 1
    try:
        player = Player.query.filter(Player.id ==
                                     player_id).first_or_404()
        agent = Agent.query.filter(Agent.id ==
                                   player.agent_id).first_or_404()

        if player is None:
            abort(404)

        return jsonify({
            'success': True,
            'player_details': player.format_extended(),
            'total_players': len(Player.query.all())
        }), 200

    except Exception as error:
        raise error


@players.route('/players', methods=['POST'])
def add_player():
    # will require authentication level 2
    try:
        body = json.loads(request.data)

        if not valid_player_body(body):
            abort(422)

        new_player = Player(**body)
        new_player.insert()

        current_players = paginate_players(request,
                                           Player.query.order_by(
                                               Player.id).all())

        return jsonify({
            'success': True,
            'new_player_id': new_player.id,
            'new_player': new_player.format_extended(),
            'players': current_players,
            'total_players': len(Player.query.all())
        }), 201

    except json.decoder.JSONDecodeError:
        abort(400)
    # except KeyError:
    #     abort(400)
    except Exception as error:
        raise error


@players.route('/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    # will require authentication level 3
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

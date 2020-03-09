import json

from flask import Blueprint, jsonify, request, abort
from sqlalchemy.exc import IntegrityError

from auth.auth import requires_auth
from ..models import Player, Agent
from .helpers import valid_player_body, valid_player_patch_body

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
@requires_auth('get:players')
def get_all_players(jwt):
    try:
        player_query = Player.query.all()

        if not player_query:
            abort(404)

        paginated_players = paginate_players(
            request, Player.query.order_by(Player.id).all())

        return jsonify({
            'success': True,
            'players': paginated_players,
            'total_players': len(player_query)
        }), 200

    except Exception as error:
        raise error


@players.route('/players/<int:player_id>/details', methods=['GET'])
@requires_auth('get:player-details')
def get_specific_player_details(jwt, player_id):
    try:
        player = Player.query.filter_by(id=player_id).first_or_404()

        return jsonify({
            'success': True,
            'player_details': player.format_extended()
        }), 200

    except Exception as error:
        raise error


@players.route('/players', methods=['POST'])
@requires_auth('post:players')
def post_player(jwt):
    try:
        body = json.loads(request.data)

        if not valid_player_body(body):
            abort(400)

        new_player = Player(**body)
        new_player.insert()

        return jsonify({
            'success': True,
            'new_player_id': new_player.id,
            'new_player': new_player.format_extended(),
            'total_players': len(Player.query.all())
        }), 201

    except json.decoder.JSONDecodeError:
        abort(400)
    except TypeError:
        abort(400)
    except Exception as error:
        raise error


@players.route('/players/<int:player_id>', methods=['DELETE'])
@requires_auth('delete:players')
def delete_player(jwt, player_id):
    try:
        player = Player.query.filter_by(id=player_id).first_or_404()

        player.delete()

        return jsonify({
            'success': True,
            'deleted_id': player.id,
            'total_players': len(Player.query.all())
        }), 200

    except Exception as error:
        raise error


@players.route('/players/<int:player_id>', methods=['PATCH'])
@requires_auth('patch:players')
def patch_player_details(jwt, player_id):
    try:
        player = Player.query.filter_by(id=player_id).first_or_404()

        body = request.get_json()

        if not valid_player_patch_body(body):
            abort(400)

        for k, v in body.items():
            setattr(player, k, v)

        player.update()

        return jsonify({
            'success': True,
            'updated_player': player.format_extended()
        }), 200

    except json.decoder.JSONDecodeError:
        abort(400)
    except IntegrityError:
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'The team_id or agent_id you entered does not exist '
                       'in the database. Please check your input and try '
                       'again.'
        }), 400
    except Exception as error:
        raise error

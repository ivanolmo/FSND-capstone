import json

from flask import Blueprint, jsonify, request, abort
from sqlalchemy.exc import IntegrityError

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
def get_all_players():
    # requires no authentication, public
    try:
        player_query = Player.query.all()

        if not player_query:
            abort(404)

        paginated_players = paginate_players(
            request, Player.query.order_by(Player.id).all())

        return jsonify({
            'success': True,
            'players': paginated_players,
            'total_players': len(paginated_players)
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
def post_player():
    # will require authentication level 2
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
        }), 200

    except Exception as error:
        raise error


@players.route('/players/<int:player_id>', methods=['PATCH'])
def patch_player_details(player_id):
    # will require authentication level 2
    try:
        player = Player.query.filter(Player.id == player_id).one_or_none()

        if player is None:
            abort(404)

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

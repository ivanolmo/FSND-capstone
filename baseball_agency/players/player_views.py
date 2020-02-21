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
    # requires no authentication
    try:
        players = Player.query.all()
        # paginated_players = paginate_players(request, players)

        if not players:
            abort(404)

        players = [player.format() for player in players]

        return jsonify({
            'success': True,
            'players': players
        }), 200

    except Exception as error:
        raise error


@players.route('/players/<int:player_id>', methods=['GET'])
def get_specific_player_details(player_id):
    # will require authentication
    try:
        player = Player.query.filter(Player.id ==
                                     player_id).one_or_none()
        agent = Agent.query.filter(Agent.id ==
                                   player.agent_id).one_or_none()

        if player is None:
            abort(404)

        return jsonify({
            'success': True,
            'player_id': player.id,
            'player_name': player.name,
            'agent_id': player.agent_id,
            'team_id': player.team_id,
            'salary': player.salary,
            'agent': agent.name
        }), 200

    except Exception as error:
        raise error


@players.route('/players', methods=['POST'])
def add_player():
    # will require authentication
    try:
        body = request.get_json()
        name = body.get('name', None)
        number = body.get('number', None)
        position = body.get('position', None)
        salary = body.get('salary', None)
        agent_id = body.get('agent_id')
        team_id = body.get('team_id')

        if not valid_player_body():
            abort(404)

        new_player = Player(name=name, number=number, position=position,
                            salary=salary, agent_id=agent_id, team_id=team_id)
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

    except Exception as error:
        raise error


@players.route('/players/<int:player_id>', methods=['DELETE'])
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

import json

from flask import Blueprint, jsonify, request, abort
from sqlalchemy.exc import IntegrityError

from ..models import Player, Team
from .helpers import valid_team_body, valid_team_patch_body

teams = Blueprint('teams', __name__)


@teams.route('/teams', methods=['GET'])
def get_all_teams():
    # no auth
    try:
        team_query = Team.query.all()

        if not team_query:
            abort(404)

        all_teams = [team.format() for team in team_query]

        return jsonify({
            'success': True,
            'teams': all_teams,
            'total_teams': len(all_teams)
        }), 200

    except Exception as error:
        raise error


@teams.route('/teams/<int:team_id>/details', methods=['GET'])
def get_specific_team_details(team_id):
    # auth level 1
    try:
        team = Team.query.filter_by(id=team_id).first_or_404()

        return jsonify({
            'success': True,
            'team_details': team.format_extended()
        }), 200

    except Exception as error:
        raise error


@teams.route('/teams/<int:team_id>/players', methods=['GET'])
def get_team_players(team_id):
    # auth level 1
    try:
        team = Team.query.filter_by(id=team_id).first_or_404()

        roster_query = Player.query.filter_by(team_id=team.id).all()

        # instead of returning 404, this will return an empty list and a
        # player count of 0
        roster = [player.format() for player in roster_query]

        return jsonify({
            'success': True,
            'team': team.name,
            'roster': roster,
            'total_team_players': len(roster)
        }), 200

    except Exception as error:
        raise error


@teams.route('/teams', methods=['POST'])
def post_team():
    # auth level 2
    try:
        body = json.loads(request.data)

        if not valid_team_body(body):
            abort(400)

        new_team = Team(**body)
        new_team.insert()

        return jsonify({
            'success': True,
            'new_team_id': new_team.id,
            'new_team': new_team.format_extended(),
            'total_teams': len(Team.query.all())
        }), 201

    except json.decoder.JSONDecodeError:
        abort(400)
    except Exception as error:
        raise error


@teams.route('/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    # auth level 3
    try:
        team = Team.query.filter(Team.id == team_id).one_or_none()

        if team is None:
            abort(404)

        player_query = Player.query.filter(Player.team_id == team.id)
        team_roster = [(player.id, player.name) for player in player_query]

        team.delete()

        return jsonify({
            'success': True,
            'deleted_id': team.id,
            'total_teams': len(Team.query.all())
        }), 200

    except IntegrityError:
        return jsonify({
            'success': False,
            'message': 'This team currently has one or more players. Please '
                       'reassign those players before deleting this team!',
            'players': team_roster,
            'total_players': len(team_roster)
        }), 422
    except Exception as error:
        raise error


@teams.route('/teams/<int:team_id>', methods=['PATCH'])
def patch_team_details(team_id):
    # auth level 2
    try:
        team = Team.query.filter(Team.id == team_id).one_or_none()

        if team is None:
            abort(404)

        body = request.get_json()

        if not valid_team_patch_body(body):
            abort(400)

        for k, v in body.items():
            setattr(team, k, v)

        team.update()

        return jsonify({
            'success': True,
            'updated_team': team.format_extended()
        }), 200

    except Exception as error:
        raise error

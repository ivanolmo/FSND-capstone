import json

from flask import jsonify, request, abort
from sqlalchemy.exc import IntegrityError

from auth.auth import requires_auth
from baseball_agency.teams import teams_bp
from .helpers import valid_team_body, valid_team_patch_body
from ..models import Player, Team


@teams_bp.route('/teams', methods=['GET'])
@requires_auth('get:teams')
def get_all_teams(jwt):
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


@teams_bp.route('/teams/<int:team_id>/details', methods=['GET'])
@requires_auth('get:team-details')
def get_specific_team_details(jwt, team_id):
    try:
        team = Team.query.filter_by(id=team_id).first_or_404()

        return jsonify({
            'success': True,
            'team_details': team.format_extended()
        }), 200

    except Exception as error:
        raise error


@teams_bp.route('/teams/<int:team_id>/roster', methods=['GET'])
@requires_auth('get:team-roster')
def get_team_players(jwt, team_id):
    try:
        team = Team.query.filter_by(id=team_id).first_or_404()

        roster_query = Player.query.filter_by(team_id=team.id).all()
        if not roster_query:
            abort(404)

        roster = [player.format() for player in roster_query]

        return jsonify({
            'success': True,
            'team': team.name,
            'roster': roster,
            'total_team_players': len(roster)
        }), 200

    except Exception as error:
        raise error


@teams_bp.route('/teams', methods=['POST'])
@requires_auth('post:teams')
def post_team(jwt):
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
    except TypeError:
        abort(400)
    except Exception as error:
        raise error


@teams_bp.route('/teams/<int:team_id>', methods=['DELETE'])
@requires_auth('delete:teams')
def delete_team(jwt, team_id):
    try:
        team = Team.query.filter_by(id=team_id).first_or_404()

        """First query players on team in case of IntegrityError, so that error
        return function can display the players on team, since a team cannot be
        deleted if it has players assigned to it."""
        player_query = Player.query.filter(Player.team_id == team.id)
        team_roster = [(f'id: {player.id}', f'name: {player.name}') for
                       player in player_query]

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
        }), 400
    except Exception as error:
        raise error


@teams_bp.route('/teams/<int:team_id>', methods=['PATCH'])
@requires_auth('patch:teams')
def patch_team_details(jwt, team_id):
    try:
        team = Team.query.filter_by(id=team_id).first_or_404()

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

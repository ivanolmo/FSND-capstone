import json

from flask import Blueprint, jsonify, request, abort

from .. import app
from ..models import Player, Team
from .helpers import valid_team_body

teams = Blueprint('teams', __name__)

TEAMS_PER_PAGE = 10


def paginate_teams(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * TEAMS_PER_PAGE
    end = start + TEAMS_PER_PAGE

    teams = [team.format() for team in selection]
    current_teams = teams[start:end]

    return current_teams


@teams.route('/teams', methods=['GET'])
def get_all_teams():
    try:
        team_query = Team.query.all()

        all_teams = [team.team_name for team in team_query]

        return jsonify({
            'success': True,
            'teams': all_teams
        }), 200

    except Exception as error:
        raise error


@teams.route('/teams/<int:team_id>', methods=['GET'])
def get_specific_team_details(team_id):
    # will require authentication level 1
    try:
        team = Team.query.filter(Team.id == team_id).first_or_404()

        if team is None:
            abort(404)

        return jsonify({
            'success': True,
            'team_details': team.format(),
            'total_teams': len(Team.query.all())
        }), 200

    except Exception as error:
        raise error


@teams.route('/teams', methods=['POST'])
def add_team():
    # will require authentication level 2
    try:
        body = json.loads(request.data)

        if not valid_team_body(body):
            abort(422)

        new_team = Team(**body)
        new_team.insert()

        current_teams = paginate_teams(request,
                                       Team.query.order_by(Team.id).all())

        return jsonify({
            'success': True,
            'new_team_id': new_team.id,
            'new_team': new_team.format(),
            'teams': current_teams,
            'total_teams': len(Team.query.all())
        }), 201

    except json.decoder.JSONDecodeError:
        abort(400)
    except Exception as error:
        raise error

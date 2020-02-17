from flask import jsonify, request, abort

from .. import app
from ..models import Player

TEAMS_PER_PAGE = 10


def paginate_players(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * TEAMS_PER_PAGE
    end = start + TEAMS_PER_PAGE

    teams = [team.format() for team in selection]
    current_teams = teams[start:end]

    return current_teams

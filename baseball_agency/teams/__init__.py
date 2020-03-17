from flask import Blueprint

teams_bp = Blueprint('teams', __name__)

from baseball_agency.teams import team_views  # noqa

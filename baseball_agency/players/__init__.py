from flask import Blueprint

players_bp = Blueprint('players', __name__)

from baseball_agency.players import player_views

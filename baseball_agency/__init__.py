import os

from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, jsonify

from .models import setup_db

# from auth.auth import requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

from . import errors


@app.route('/', methods=['GET'])
def index():
    # TODO remove this placeholder test endpoint when done
    return jsonify({
        'success': True,
        'message': 'index page works'
    }), 200


# project_folder = os.path.join(os.path.dirname(__file__), '..')
# load_dotenv(os.path.join(project_folder, '.env'))


# set up flask blueprints
from .players.player_views import players
from .teams.team_views import teams
from .agents.agent_views import agents

app.register_blueprint(players)
app.register_blueprint(teams)
app.register_blueprint(agents)

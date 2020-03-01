from flask_cors import CORS
from flask import Flask, jsonify

from .models import setup_db

# from auth.auth import requires_auth

# db_drop_and_create_all()

app = Flask(__name__)
setup_db(app)
# CORS(app, resource={r'/api/*': {'origins': '*'}})
CORS(app)

from . import errors

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Headers',
#                          'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods',
#                          'GET,POST,PATCH,DELETE,OPTIONS')
#     return response


@app.route('/', methods=['GET'])
def index():
    # TODO remove this placeholder test endpoint when done
    return jsonify({
        'success': True,
        'message': 'index page works'
    }), 200


# set up flask blueprints
from .players.player_views import players
from .teams.team_views import teams
from .agents.agent_views import agents

app.register_blueprint(players)
app.register_blueprint(teams)
app.register_blueprint(agents)

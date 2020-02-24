from flask import Blueprint, jsonify, request, abort

from .. import app
from ..models import Player, Team, Agent

agents = Blueprint('agents', __name__)

AGENTS_PER_PAGE = 10


def paginate_players(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * AGENTS_PER_PAGE
    end = start + AGENTS_PER_PAGE

    agents = [agent.format() for agent in selection]
    current_agents = agents[start:end]

    return current_agents


@agents.route('/agents', methods=['GET'])
def get_all_agents():
    agents_query = Agent.query.all()

    all_agents = [agent.format() for agent in agents_query]

    return jsonify({
        'success': True,
        'agents': all_agents
    }), 200

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
    try:
        agents_query = Agent.query.all()

        all_agents = [agent.format() for agent in agents_query]

        return jsonify({
            'success': True,
            'agents': all_agents
        }), 200

    except Exception as error:
        raise error


@agents.route('/agents/<int:agent_id>', methods=['GET'])
def get_specific_agent(agent_id):
    # will require authentication level 1
    try:
        agent = Agent.query.filter(Agent.id ==
                                   agent_id).first_or_404()

        if agent is None:
            abort(404)

        return jsonify({
            'success': True,
            'agent': agent.format()
        }), 200

    except Exception as error:
        raise error

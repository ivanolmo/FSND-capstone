import json

from flask import Blueprint, jsonify, request, abort

from .. import app
from ..models import Player, Team, Agent
from .helpers import valid_agent_body

agents = Blueprint('agents', __name__)

AGENTS_PER_PAGE = 10


def paginate_agents(request, selection):
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


@agents.route('/agents', methods=['POST'])
def add_agent():
    # will require authentication level 3
    try:
        body = json.loads(request.data)

        if not valid_agent_body(body):
            abort(422)

        new_agent = Agent(**body)
        new_agent.insert()

        current_agents = paginate_agents(request, Agent.query.order_by(
            Agent.id).all())

        return jsonify({
            'success': True,
            'new_agent_id': new_agent.id,
            'new_agent': new_agent.format(),
            'agents': current_agents,
            'total_agents': len(Agent.query.all())
        }), 201

    except json.decoder.JSONDecodeError:
        abort(400)
    except Exception as error:
        raise error


@agents.route('/agents/<int:agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    # will require authentication level 3
    try:
        agent = Agent.query.filter(Agent.id == agent_id).one_or_none()

        if agent is None:
            abort(404)

        agent.delete()

        return jsonify({
            'success': True,
            'deleted_id': agent.id,
            'total_agents': len(Agent.query.all())
        }), 200

    except Exception as error:
        raise error

import json

from flask import Blueprint, jsonify, request, abort
from sqlalchemy.exc import IntegrityError

from ..models import Player, Agent
from .helpers import valid_agent_body, valid_agent_patch_body

agents = Blueprint('agents', __name__)


@agents.route('/agents', methods=['GET'])
def get_all_agents():
    # auth level 1
    try:
        agents_query = Agent.query.all()

        if not agents_query:
            abort(404)

        all_agents = [agent.format() for agent in agents_query]

        return jsonify({
            'success': True,
            'agents': all_agents,
            'total_agents': len(all_agents)
        }), 200

    except Exception as error:
        raise error


@agents.route('/agents/<int:agent_id>/details', methods=['GET'])
def get_specific_agent_details(agent_id):
    # auth level 2
    try:
        agent = Agent.query.filter_by(id=agent_id).first_or_404()

        return jsonify({
            'success': True,
            'agent': agent.format_extended()
        }), 200

    except Exception as error:
        raise error


@agents.route('/agents/<int:agent_id>/clients', methods=['GET'])
def get_agent_clients(agent_id):
    # auth level 2
    try:
        agent = Agent.query.filter_by(id=agent_id).first_or_404()

        client_query = Player.query.filter_by(agent_id=agent.id).all()

        # instead of returning 404, this will return an empty list and a
        # client count of 0
        clients = [player.format() for player in client_query]

        return jsonify({
            'success': True,
            'agent': agent.name,
            'clients': clients,
            'total_agent_clients': len(clients)
        }), 200

    except Exception as error:
        raise error


@agents.route('/agents', methods=['POST'])
def post_agent():
    # auth level 3
    try:
        body = json.loads(request.data)

        if not valid_agent_body(body):
            abort(400)

        new_agent = Agent(**body)
        new_agent.insert()

        return jsonify({
            'success': True,
            'new_agent_id': new_agent.id,
            'new_agent': new_agent.format_extended(),
            'total_agents': len(Agent.query.all())
        }), 201

    except json.decoder.JSONDecodeError:
        abort(400)
    except Exception as error:
        raise error


@agents.route('/agents/<int:agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    # auth level 3
    try:
        agent = Agent.query.filter_by(id=agent_id).first_or_404()

        """Query players assigned to agent in case of IntegrityError, 
        so that the error return function can display players assigned to 
        agent. An agent cannot be deleted if it has players assigned to it."""
        player_query = Player.query.filter(Player.agent_id == agent.id)
        client_list = [(f'id: {client.id}', f'name: {client.name}') for client
                       in player_query]

        agent.delete()

        return jsonify({
            'success': True,
            'deleted_id': agent.id,
            'total_agents': len(Agent.query.all())
        }), 200

    except IntegrityError:
        return jsonify({
            'success': False,
            'message': 'This agent currently represents one or more players. '
                       'Please reassign those players before deleting this '
                       'agent!',
            'clients': client_list,
            'total_clients': len(client_list)
        })
    except Exception as error:
        raise error


@agents.route('/agents/<int:agent_id>', methods=['PATCH'])
def patch_agent_details(agent_id):
    # auth level 3
    try:
        agent = Agent.query.filter_by(id=agent_id).first_or_404()

        body = request.get_json()

        if not valid_agent_patch_body(body):
            abort(400)

        for k, v in body.items():
            setattr(agent, k, v)

        agent.update()

        return jsonify({
            'success': True,
            'updated_agent': agent.format_extended()
        }), 200

    except Exception as error:
        raise error

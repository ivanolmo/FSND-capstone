from flask import Blueprint

agents_bp = Blueprint('agents', __name__)

from baseball_agency.agents import agent_views  # noqa

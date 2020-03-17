from flask import Blueprint

errors_bp = Blueprint('errors', __name__)

from baseball_agency.errors import handlers

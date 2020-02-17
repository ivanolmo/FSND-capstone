from flask_cors import CORS
from flask import Flask, request, jsonify, abort

from baseball_agency.models import Player, setup_db

# from auth.auth import requires_auth

# db_drop_and_create_all()

PLAYERS_PER_PAGE = 10


# def create_app(test_config=None):
app = Flask(__name__)
setup_db(app)
# CORS(app, resource={r'/api/*': {'origins': '*'}})
CORS(app)





# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Headers',
#                          'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods',
#                          'GET,POST,PATCH,DELETE,OPTIONS')
#     return response


@app.route('/', methods=['GET'])
def index():
    # placeholder test endpoint
    return jsonify({
        'success': True,
        'message': 'Cool, it works'
    }), 200




    # return app


from . import errors

# if __name__ == '__main__':
#     create_app()

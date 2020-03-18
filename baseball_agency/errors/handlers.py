from flask import jsonify

from auth.auth import AuthError
from baseball_agency.errors import errors_bp
from .. import db


@errors_bp.app_errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": error.description
    }), 404


@errors_bp.app_errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': error.description
    }), 401


@errors_bp.app_errorhandler(403)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': error.description
    }), 403


@errors_bp.app_errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": error.description
    }), 422


@errors_bp.app_errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": error.description
    }), 400


@errors_bp.app_errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": error.description
    }), 405


@errors_bp.app_errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return jsonify({
        "success": False,
        "error": 500,
        "message": error.description
    }), 500


@errors_bp.app_errorhandler(503)
def internal_server_error(error):
    """Added because of occasional Heroku latency causing this error"""
    db.session.rollback()
    return jsonify({
        "success": False,
        "error": 503,
        "message": error.description
    }), 503


@errors_bp.app_errorhandler(AuthError)
def authentication_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error
    }), error.status_code

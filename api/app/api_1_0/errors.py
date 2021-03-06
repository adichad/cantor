from flask import jsonify

from app.api_1_0 import api
from app.errors import CatalogException


@api.app_errorhandler(404)
def page_not_found(e):
    response = jsonify({"error": "not found"})
    response.status_code = 404
    return response


@api.app_errorhandler(403)
def forbidden(message):
    response = jsonify({"error": "forbidden"})
    response.status_code = 403
    return response

@api.app_errorhandler(500)
def internal_server_error(e):
    response = jsonify({"error": "internal server error"})
    response.status_code = 403
    return response

@api.app_errorhandler(400)
def bad_request(message):
    response = jsonify({"error": "bad request"})
    response.status_code = 400
    return response


def json_error(message):
    response = jsonify({"error": message})
    response.status_code = 403
    return response

@api.errorhandler(CatalogException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response



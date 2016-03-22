import logging
from datetime import datetime

from app.api_1_0 import api
from app.decorator import json

logger = logging.getLogger()

@api.route("/status", methods=["GET"])
@json
def get_status():
    pass

@api.route("/status/<status_id>", methods=["GET"])
@json
def get_status_by_id(status_id):
    pass

@api.route("/unit", methods=["GET"])
@json
def get_unit():
    pass

@api.route("/unit/<unit_id>", methods=["GET"])
@json
def get_unit_by_id(unit_id):
    pass


@api.route("/unit>", methods=["POST"])
@json
def create_unit_id(unit_id):
    pass

@api.route("/unit>", methods=["PUT"])
@json
def update_unit_id():
    pass




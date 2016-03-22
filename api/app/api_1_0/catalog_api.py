import logging
from datetime import datetime

from flask import  request
import  ujson

from app.api_1_0 import api
from app.decorator import json
from app.src.unit import Unit, Status

logger = logging.getLogger()

@api.route("/status", methods=["GET"])
@json
def get_status():
    result = Status().get_list()
    return result

@api.route("/status/<status_id>", methods=["GET"])
@json
def get_status_by_id(status_id):
    stat = Status(status_id)
    return stat.get()

@api.route("/unit", methods=["GET"])
@json
def get_unit():
    result = Unit().get_list()
    return result

@api.route("/unit/<unit_id>", methods=["GET"])
@json
def get_unit_by_id(unit_id):
    unit = Unit(unit_id)
    return unit.get()


@api.route("/unit", methods=["POST"])
@json
def create_unit_id():
    logger.debug(request.data)
    return Unit().create(ujson.loads(request.data))

@api.route("/unit", methods=["PUT"])
@json
def update_unit_id():
    logger.debug(request.data)
    data = ujson.loads(request.data)
    id = data["id"]
    del(data["id"])
    return Unit(id).update(data)




import logging
from datetime import datetime

from flask import  request
from webargs import fields, validate
from webargs.flaskparser import parser
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
    """
    {
        "name":"unit name",
        "status_id":1
    }
    """
    unit_args = {
        "name"          : fields.Str(required=True),
        "status_id"     : fields.Int(required=True)
    }
    logger.debug(request.data)
    args = parser.parse(unit_args, request)
    logger.debug(args)
    return Unit().create(args)

@api.route("/unit", methods=["PUT"])
@json
def update_unit_id():
    unit_args = {
        "id"        : fields.Int(required=True),
        "name"      : fields.Str(required=False),
        "status_id" : fields.Int(required=False)
    }
    logger.debug(request.data)
    args = parser.parse(unit_args, request)
    logger.debug(args)
    data = args
    id = data["id"]
    del(data["id"])
    return Unit(id).update(data)




import logging
from datetime import datetime

from flask import  request
from webargs import fields, validate
from webargs.flaskparser import parser
import  ujson

from app.api_1_0 import api
from app.decorator import json
from app.src.unit import Unit

logger = logging.getLogger()

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
    return Unit().create_unit(args)

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
    return Unit(id).update_unit(data)


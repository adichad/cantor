import logging
import binascii
from datetime import datetime

from flask import  request
from webargs import fields, validate
from webargs.flaskparser import parser
import ujson
from app.api_1_0 import api
from app.decorator import json
from app.src.hub_serviceability import HubServiceability

logger = logging.getLogger()

@api.route("/hub_serviceability/<pageno>/<pagesize>", methods=["GET"])
@json
def get_hub_serviceability_list(pageno, pagesize):
    pageno = int(pageno)
    pagesize = int(pagesize)

    offset = (pageno-1) * pagesize
    limit = pagesize

    hub_serviceability_list, total_records = HubServiceability().get_detailed_list(limit, offset)
    result = {'total_records':total_records, 'data':hub_serviceability_list}
    return result

@api.route("/hub_serviceability", methods=["POST"])
@json
def create_hub_serviceability():
    hub_serviceability_args = {
        "hub_geo_id"        : fields.Int(required=True),
        "serviceable_geo_id": fields.Int(required=True),
        "status_id"         : fields.Int(required=True)
    }
    logger.debug(request.data)
    args = parser.parse(hub_serviceability_args, request)
    hub_serviceability = HubServiceability().create(args)
    return hub_serviceability

@api.route("/hub_serviceability", methods=["PUT"])
@json
def update_hub_serviceability():
    hub_serviceability_args = {
        "id"        : fields.Int(required=True),
        "status_id" : fields.Int(required=False)
    }
    logger.debug(request.data)
    args = parser.parse(hub_serviceability_args, request)
    logger.debug(args)
    data = args
    id = data["id"]
    del(data["id"])
    return HubServiceability(id).update(data)


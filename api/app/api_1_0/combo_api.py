import logging
import binascii
from datetime import datetime

from flask import  request
from webargs import fields, validate
from webargs.flaskparser import parser
import ujson
from app.api_1_0 import api
from app.decorator import json
from app.src.combo import Combo

logger = logging.getLogger()

@api.route("/combo/<pageno>/<pagesize>", methods=["GET"])
@json
def get_combo_list(pageno, pagesize):
    result = Combo().get_list()
    for r in result:
        r['uuid'] = binascii.hexlify(r['uuid'])
    return result

@api.route("/combo/<combo_id>", methods=["GET"])
@json
def get_combo_by_id(combo_id):
    combo = Combo(combo_id)
    combo_details = combo.get()
    combo_details['uuid'] = binascii.hexlify(combo_details['uuid'])
    return combo_details

@api.route("/combo", methods=["POST"])
@json
def create_combo():
    combo_args = {
        "name"          : fields.Str(required=True),
        "description"   : fields.Str(required=True),
        "status_id"     : fields.Int(required=True),
        "entities"      : fields.List(fields.Nested({
                            'entity_id'     : fields.Int(required=True),
                            'entity_type'   : fields.Str(required=True),
                            'quantity'      : fields.Int(required=True),
                        }), required=True, validate=lambda p: len(p) >= 1)
    }
    logger.debug(request.data)
    args = parser.parse(combo_args, request)
    logger.debug(args)
    combo = Combo().create_combo(args)
    combo['uuid'] = binascii.hexlify(combo['uuid'])
    return combo


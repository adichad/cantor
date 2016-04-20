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
    pageno = int(pageno)
    pagesize = int(pagesize)

    start_index = (pageno-1) * pagesize
    end_index = start_index + pagesize

    combo_list = Combo().get_list()
    for combo in combo_list[start_index:end_index]:
        combo['uuid'] = binascii.hexlify(combo['uuid'])

    result = {'total_records':len(combo_list), 'data':combo_list[start_index:end_index]}
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


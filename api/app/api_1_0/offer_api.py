import logging
from datetime import datetime

from flask import  request
from webargs import fields, validate
from webargs.flaskparser import parser
import ujson
from app.api_1_0 import api
from app.decorator import json
from app.src.offer import Offer

logger = logging.getLogger()

@api.route("/offer/<pageno>/<pagesize>", methods=["GET"])
@json
def get_offer_list(pageno, pagesize):
    result = Offer().get_list()
    return result

@api.route("/offer/<offer_id>", methods=["GET"])
@json
def get_offer_by_id(offer_id):
    result = Offer(offer_id)
    return result.get()


@api.route("/offer", methods=["POST"])
@json
def create_offer():
    """
    {
        "subscription_ids":[1],
        "discount_percent":10,
        "discount_cap_amount":10,
        "valid_from":"1970-01-01 00:00:00",
        "valid_thru":"1970-01-01 00:00:00",
        "status_id":1
    }
    """
    offer_args = {
        "entity_id"             : fields.Int(required=True),
        "entity_type"           : fields.Str(required=True, validate=lambda v: v in ['product', 'variant', 'subscription', 'combo']),
        "quantity"              : fields.Int(required=True),
        "discount_percent"      : fields.Float(required=True),
        "discount_cap_amount"   : fields.Float(required=True),
        "valid_from"            : fields.Str(required=True),
        "valid_thru"            : fields.Str(required=True),
        "status_id"             : fields.Int(required=True),
    }
    logger.debug(request.data)
    args = parser.parse(offer_args, request)
    logger.debug(args)
    return Offer().create(args)

@api.route("/offer", methods=["PUT"])
@json
def update_offer():
    """
    {
        "id":1,
        "discount_percent":10,
        "discount_cap_amount":10,
        "valid_from":"1970-01-01 00:00:00",
        "valid_thru":"1970-01-01 00:00:00",
        "status_id":1
    }
    """
    offer_args = {
        "id"                    : fields.Int(required=True),
        "quantity"              : fields.Int(required=False),
        "discount_percent"      : fields.Float(required=False),
        "discount_cap_amount"   : fields.Float(required=False),
        "valid_from"            : fields.Str(required=False),
        "valid_thru"            : fields.Str(required=False),
        "status_id"             : fields.Int(required=False)
    }
    logger.debug(request.data)
    args = parser.parse(offer_args, request)
    logger.debug(args)
    data = args
    id = data["id"]
    del(data["id"])
    return Offer(id).update(data)


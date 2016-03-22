import logging
from datetime import datetime

from flask import  request
import ujson
from app.api_1_0 import api
from app.decorator import json
from app.src.offer import Offer

logger = logging.getLogger()

@api.route("/offer/<pageno>/<pagesize>", methods=["GET"])
@json
def get_offer_list(pageno=1,pagesize=10):
    result = Offer().get_list()
    return result

@api.route("/offer/<offer_id>", methods=["GET"])
@json
def get_offer_by_id(offer_id):
    cat = Offer(offer_id)
    return cat.get()


@api.route("/offer", methods=["POST"])
@json
def create_offer():
    logger.debug(request.data)
    return Offer().create(ujson.loads(request.data))

@api.route("/offer", methods=["PUT"])
@json
def update_offer():
    logger.debug(request.data)
    data = ujson.loads(request.data)
    id = data["id"]
    del(data["id"])
    return Offer(id).update(data)


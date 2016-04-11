import logging
import binascii
from datetime import datetime

from flask import  request
import ujson
from app.api_1_0 import api
from app.decorator import json
from app.src.subscription import Subscription

logger = logging.getLogger()

@api.route("/subscription/<pageno>/<pagesize>", methods=["GET"])
@json
def get_subscription_list(pageno, pagesize):
    result = Subscription().get_list()
    for r in result:
        r['uuid'] = binascii.hexlify(r['uuid'])
    return result


@api.route("/subscription/<subscription_id>", methods=["GET"])
@json
def get_subscription_by_id(subscription_id):
    sub = Subscription(subscription_id)
    subscription = sub.get()
    subscription['uuid'] = binascii.hexlify(subscription['uuid'])
    return subscription


@api.route("/subscription", methods=["POST"])
@json
def create_subscription():
    logger.debug(request.data)
    subscription = Subscription().create_subscription(ujson.loads(request.data))
    subscription['uuid'] = binascii.hexlify(subscription['uuid'])
    return subscription


@api.route("/subscription", methods=["PUT"])
@json
def update_subscription():
    logger.debug(request.data)
    data = ujson.loads(request.data)
    id = data["id"]
    del(data["id"])
    return Subscription(id).update(data)


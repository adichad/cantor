import logging
import binascii
from datetime import datetime

from flask import  request
from webargs import fields, validate
from webargs.flaskparser import parser
import ujson
from app.api_1_0 import api
from app.decorator import json
from app.src.subscription import Subscription

logger = logging.getLogger()

@api.route("/subscription/<pageno>/<pagesize>", methods=["GET"])
@json
def get_subscription_list(pageno, pagesize):
    pageno = int(pageno)
    pagesize = int(pagesize)

    start_index = (pageno-1) * pagesize
    end_index = start_index + pagesize

    subscription_list = Subscription().get_list()
    for subscription in subscription_list[start_index:end_index]:
        subscription['uuid'] = binascii.hexlify(subscription['uuid'])

    result = {'total_records':len(subscription_list), 'data':subscription_list[start_index:end_index]}
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

@api.route("/subscription/<subscription_id>/condition", methods=["GET"])
@json
def get_conditions_by_subscription_by_id(subscription_id):
    subscription = Subscription(subscription_id)
    conditions = subscription.get_conditions()
    return conditions

@api.route("/subscription/<subscription_id>/condition", methods=["POST"])
@json
def attach_condition_to_subscription(subscription_id):
    condition_args = {
        "condition_id"  : fields.Int(required=True),
        "status_id"     : fields.Int(required=True)
    }
    logger.debug(request.data)
    args = parser.parse(condition_args, request)
    logger.debug(args)
    subscription = Subscription(subscription_id)
    conditions = subscription.attach_condition(args)
    return conditions

@api.route("/subscription/<subscription_id>/shipping_type", methods=["GET"])
@json
def get_shipping_types_by_subscription_by_id(subscription_id):
    subscription = Subscription(subscription_id)
    shipping_types = subscription.get_shipping_types()
    return shipping_types

@api.route("/subscription/<subscription_id>/shipping_type", methods=["POST"])
@json
def attach_shipping_type_to_subscription(subscription_id):
    condition_args = {
        "condition_id"  : fields.Int(required=True),
        "status_id"     : fields.Int(required=True)
    }
    logger.debug(request.data)
    args = parser.parse(condition_args, request)
    logger.debug(args)
    subscription = Subscription(subscription_id)
    conditions = subscription.attach_condition(args)
    return conditions


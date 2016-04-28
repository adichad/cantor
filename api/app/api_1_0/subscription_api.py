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

    offset = (pageno-1) * pagesize
    limit = pagesize

    subscription_list, total_records = Subscription().get_detailed_list(limit, offset)
    for subscription in subscription_list:
        subscription['uuid'] = binascii.hexlify(subscription['uuid'])
        subscription['variant']['uuid'] = binascii.hexlify(subscription['variant']['uuid'])

    result = {'total_records':total_records, 'data':subscription_list}
    return result


@api.route("/subscription/<subscription_id>", methods=["GET"])
@json
def get_subscription_by_id(subscription_id):
    sub = Subscription(subscription_id)
    subscription = sub.get_details()
    subscription['uuid'] = binascii.hexlify(subscription['uuid'])
    subscription['variant']['uuid'] = binascii.hexlify(subscription['variant']['uuid'])
    logger.debug(subscription)
    return subscription


@api.route("/subscription", methods=["POST"])
@json
def create_subscription():
    subscription_args = {
        "variant_id"                : fields.Int(required=True),
        "seller_id"                 : fields.Int(required=True),
        "transfer_price"            : fields.Float(required=True),
        "take_rate"                 : fields.Float(required=True),
        "seller_indicated_price"    : fields.Float(required=True),
        "quantity_available"        : fields.Int(required=True),
        "valid_from"                : fields.Str(required=True),
        "valid_thru"                : fields.Str(required=True),
        "status_id"                 : fields.Int(required=True)
    }
    logger.debug(request.data)
    args = parser.parse(subscription_args, request)
    subscription = Subscription().create_subscription(args)
    subscription['uuid'] = binascii.hexlify(subscription['uuid'])
    return subscription


@api.route("/subscription", methods=["PUT"])
@json
def update_subscription():
    subscription_args = {
        "id"                        : fields.Int(required=True),
        "variant_id"                : fields.Int(required=False),
        "seller_id"                 : fields.Int(required=False),
        "transfer_price"            : fields.Float(required=False),
        "take_rate"                 : fields.Float(required=False),
        "seller_indicated_price"    : fields.Float(required=False),
        "quantity_available"        : fields.Int(required=False),
        "valid_from"                : fields.Str(required=False),
        "valid_thru"                : fields.Str(required=False),
        "status_id"                 : fields.Int(required=False)
    }
    logger.debug(request.data)
    args = parser.parse(subscription_args, request)
    logger.debug(args)
    data = args
    id = data["id"]
    del(data["id"])

    updated_subscription = Subscription(id).update(data)
    updated_subscription['uuid'] = binascii.hexlify(updated_subscription['uuid'])
    return updated_subscription

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


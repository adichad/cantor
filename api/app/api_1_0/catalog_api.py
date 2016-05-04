import logging
from datetime import datetime

from flask import  request
from webargs import fields, validate
from webargs.flaskparser import parser
import  ujson

from app.api_1_0 import api
from app.decorator import json
from app.src.unit import Unit, Status
from app.src.catalog import Catalog
from app.src.seller import Seller
from app.src.condition import Condition
from app.src.shipping_type import ShippingType

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

@api.route("/search/<uuid>", methods=["GET"])
@json
def search_by_uuid(uuid):
    return Catalog.search(uuid)

@api.route("/calculate_price", methods=["POST"])
@json
def calculate_price_by_uuid():
    price_args = {
        "geo_id"    : fields.Str(required=True),
        "items"     : fields.List(fields.Nested({
                            'item_uuid' : fields.Str(required=True),
                            'quantity'  : fields.Int(required=True)
                        }), required=True, validate=lambda p: len(p) >= 1)
            }
    logger.debug(request.data)
    args = parser.parse(price_args, request)
    logger.debug(args)
    return Catalog.calculate_price(args)

@api.route("/reconcile_uuid_entity_ref", methods=["GET"])
@json
def reconcile_uuid_entity_ref():
    return Catalog.reconcile_uuid_entity_ref()

@api.route("/seller", methods=["GET"])
@json
def get_sellers():
    result = Seller().get_list()
    return result

@api.route("/seller/<seller_id>", methods=["GET"])
@json
def get_seller_details(seller_id):
    seller = Seller(seller_id)
    return seller.get()

@api.route("/seller", methods=["POST"])
@json
def create_seller():
    """
    {
        `name`
        `description`
        `address`
        `voice_contact`
        `email`
        `status_id`
    }
    """
    seller_args = {
        "name"          : fields.Str(required=True),
        "description"   : fields.Str(required=True),
        "address"       : fields.Str(required=True),
        "voice_contact" : fields.Str(required=True),
        "email"         : fields.Str(required=True),
        "status_id"     : fields.Int(required=True)
    }
    logger.debug(request.data)
    args = parser.parse(seller_args, request)
    logger.debug(args)
    return Seller().create(args)

@api.route("/seller", methods=["PUT"])
@json
def update_seller():
    seller_args = {
        "id"            : fields.Int(required=True),
        "name"          : fields.Str(required=False),
        "description"   : fields.Str(required=False),
        "address"       : fields.Str(required=False),
        "voice_contact" : fields.Str(required=False),
        "email"         : fields.Str(required=False),
        "status_id"     : fields.Int(required=False)
    }
    logger.debug(request.data)
    args = parser.parse(seller_args, request)
    logger.debug(args)
    data = args
    id = data["id"]
    del(data["id"])
    return Seller(id).update(data)

@api.route("/condition", methods=["GET"])
@json
def get_conditions():
    result = Condition().get_list()
    return result

@api.route("/condition/<condition_id>", methods=["GET"])
@json
def get_condition_details(condition_id):
    condition = Condition(condition_id)
    return condition.get()

@api.route("/condition", methods=["POST"])
@json
def create_condition():
    """
    {
        `name`
        `description`
        `address`
        `voice_contact`
        `email`
        `status_id`
    }
    """
    condition_args = {
        "name"          : fields.Str(required=True),
        "description"   : fields.Str(required=True),
        "status_id"     : fields.Int(required=True)
    }
    logger.debug(request.data)
    args = parser.parse(condition_args, request)
    logger.debug(args)
    return Condition().create(args)

@api.route("/condition", methods=["PUT"])
@json
def update_condition():
    condition_args = {
        "id"            : fields.Int(required=True),
        "description"   : fields.Str(required=False),
        "status_id"     : fields.Int(required=False)
    }
    logger.debug(request.data)
    args = parser.parse(condition_args, request)
    logger.debug(args)
    data = args
    id = data["id"]
    del(data["id"])
    return Condition(id).update(data)

@api.route("/shipping_type", methods=["GET"])
@json
def get_shipping_types():
    result = ShippingType().get_list()
    return result

@api.route("/entity_type", methods=["GET"])
@json
def get_entity_types():
    result = ['combo', 'product', 'variant', 'subscription']
    return result

@api.route("/value_type", methods=["GET"])
@json
def get_value_types():
    result = ['varchar', 'int', 'bigint', 'char', 'float', 'double', 'decimal', 'date', 'time', 'datetime']
    return result

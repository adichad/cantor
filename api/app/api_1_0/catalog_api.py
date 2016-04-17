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
    return Unit().create(args)

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
    return Unit(id).update(data)

@api.route("/search/<uuid>", methods=["GET"])
@json
def search_by_uuid(uuid):
    return Catalog.search(uuid)

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


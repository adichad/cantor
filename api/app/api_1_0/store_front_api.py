import logging
from datetime import datetime

from flask import  request
from webargs import fields, validate
from webargs.flaskparser import parser
import ujson
from app.api_1_0 import api
from app.decorator import json
from app.src.store_front import StoreFront

logger = logging.getLogger()

@api.route("/storefront", methods=["GET"])
@json
def get_store_front_list():
    result = StoreFront().get_list()
    return result


@api.route("/storefront/<store_front_id>", methods=["GET"])
@json
def get_store_front_by_id(store_front_id):
    sf = StoreFront(store_front_id)
    return sf.get()

@api.route("/storefront", methods=["POST"])
@json
def create_store_front():
    """
    {
        "name":
        "description":
        "meta_tags":
        "template":
        "status_id": 1
    }
    """
    store_front_args = {
        "name"          : fields.Str(required=True),
        "description"   : fields.Str(required=True),
        "meta_tags"     : fields.Str(required=True),
        "template"      : fields.Str(required=True),
        "status_id"     : fields.Int(required=True)
    }
    logger.debug(request.data)
    args = parser.parse(store_front_args, request)
    logger.debug(args)
    return StoreFront().create(args)

@api.route("/storefront", methods=["PUT"])
@json
def update_store_front():
    """
    {
        "parent_id": 0,
        "name": "new category name",
        "description": "description of new category",
        "status_id": 1,
        "id":1
    }
    """
    store_front_args = {
        "name"          : fields.Str(required=False),
        "description"   : fields.Str(required=False),
        "meta_tags"     : fields.Str(required=False),
        "template"      : fields.Str(required=False),
        "status_id"     : fields.Int(required=False),
        "id"            : fields.Int(required=True)
    }
    logger.debug(request.data)
    args = parser.parse(store_front_args, request)
    logger.debug(args)
    data = args
    id = data["id"]
    del(data["id"])
    return StoreFront(id).update(data)

@api.route("/storefront/<store_front_id>/entity", methods=["GET"])
@json
def get_store_front_id_entity_map(store_front_id):
    return StoreFront(store_front_id).get_store_front_id_entity_map()

@api.route("/storefront/<store_front_id>/entity", methods=["POST"])
@json
def store_front_attribute_map(store_front_id):
    """
        [
            {
                "entity_type"   :"",
                "entity_id"     :1,
                "display_order" :2
            }
        ]
    """
    logger.debug(request.data)
    data = ujson.loads(request.data)
    return StoreFront(store_front_id).update_store_front_id_entity_map(data)


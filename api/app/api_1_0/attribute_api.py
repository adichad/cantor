import logging

from flask import request
import ujson

from app.api_1_0 import api
from app.decorator import json
from app.src.attribute import Attribute

logger = logging.getLogger()


@api.route("/attribute", methods=["GET"])
@json
def get_attribute_list():
    result = Attribute().get_list()
    return result


@api.route("/attribute/<attribute_id>", methods=["GET"])
@json
def get_attribute_by_id(attribute_id):
    attr = Attribute(attribute_id)
    return attr.get()


@api.route("/attribute", methods=["POST"])
@json
def create_attribute():
    """
    {
        "name":"attribute name",
        "value_type":'int'
        "constraint":''
        "cardinality":'one/many'
        "description":''
        "validation":'strict/free'
        "status_id":1
    }
    """
    logger.debug(request.data)
    return Attribute().create(ujson.loads(request.data))


@api.route("/attribute", methods=["PUT"])
@json
def update_attribute():
    """
    {
        "id":1
        "name":"attribute name",
        "value_type":'int'
        "constraint":''
        "cardinality":'one/many'
        "description":''
        "validation":'strict/free'
        "status_id":1
    }
    """
    logger.debug(request.data)
    data = ujson.loads(request.data)
    id = data["id"]
    del(data["id"])
    return Attribute(id).update(data)



@api.route("/attribute/<attribute_id>/unit", methods=["GET"])
@json
def get_attribute_unit(attribute_id):
    attr = Attribute(attribute_id)
    return attr.get_unit()

@api.route("/attribute/<attribute_id>/unit", methods=["POST"])
@json
def create_attribute_unit_map(attribute_id):
    """
    [
        {
            "unit_id":1,
            "status_id":1
        }
    ]
    """
    attr = Attribute(attribute_id)
    logger.debug(request.data)
    data = ujson.loads(request.data)
    return attr.add_unit_map(data)

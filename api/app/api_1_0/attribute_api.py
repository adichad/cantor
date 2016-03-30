import logging

from flask import request
from webargs import fields, validate
from webargs.flaskparser import parser
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
    attribute_args = {
        "name"          : fields.Str(required=True),
        "description"   : fields.Str(required=True),
        "value_type"    : fields.Str(required=True, validate=lambda v: v in ['varchar', 'int', 'bigint', 'char', 'float', 'double', 'decimal', 'date', 'time', 'datetime']),
        "status_id"     : fields.Int(required=True),
        "constraint"    : fields.Constant(""),
        "cardinality"   : fields.Constant("many"),
        "validation"    : fields.Constant("free")
    }
    logger.debug(request.data)
    args = parser.parse(attribute_args, request)
    logger.debug(args)
    return Attribute().create(args)


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
    attribute_args = {
        "id"            : fields.Int(required=True),
        "name"          : fields.Str(required=False),
        "value_type"    : fields.Str(required=False, validate=lambda v: v in ['varchar', 'int', 'bigint', 'char', 'float', 'double', 'decimal', 'date', 'time', 'datetime']),
        "description"   : fields.Str(required=False),
        "status_id"     : fields.Int(required=False)
    }
    logger.debug(request.data)
    args = parser.parse(attribute_args, request)
    logger.debug(args)
    data = args
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
    attribute_unit_map_args = {
        "unit_id"   : fields.Int(required=True),
        "status_id" : fields.Str(required=True)
    }
    attr = Attribute(attribute_id)
    logger.debug(request.data)
    data = ujson.loads(request.data)
    return attr.add_unit_map(data)

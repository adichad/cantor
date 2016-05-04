import logging
from datetime import datetime

from flask import  request
from webargs import fields, validate
from webargs.flaskparser import parser
import ujson
from app.api_1_0 import api
from app.decorator import json
from app.src.category import Category

logger = logging.getLogger()

@api.route("/category", methods=["GET"])
@json
def get_category_list():
    result = Category().get_list()
    for r in result:
        parent = Category(r['parent_id'])
        r['parent'] = parent.get()
    return result


@api.route("/category/<category_id>", methods=["GET"])
@json
def get_category_by_id(category_id):
    cat = Category(category_id)
    category_details = cat.get()
    parent = Category(category_details['parent_id'])
    category_details['parent'] = parent.get()
    return category_details


@api.route("/category", methods=["POST"])
@json
def create_category():
    """
    {
        "parent_id": 0,
        "name": "new category name",
        "description": "description of new category",
        "status_id": 1
    }
    """
    category_args = {
        "name"          : fields.Str(required=True),
        "description"   : fields.Str(required=True),
        "parent_id"     : fields.Int(required=True),
        "status_id"     : fields.Int(required=True)
    }
    logger.debug(request.data)
    args = parser.parse(category_args, request)
    logger.debug(args)
    return Category().create(args)

@api.route("/category", methods=["PUT"])
@json
def update_category():
    """
    {
        "parent_id": 0,
        "name": "new category name",
        "description": "description of new category",
        "status_id": 1,
        "id":1
    }
    """
    category_args = {
        "id"            : fields.Int(required=True),
        "name"          : fields.Str(required=False),
        "description"   : fields.Str(required=False),
        "parent_id"     : fields.Int(required=False),
        "status_id"     : fields.Int(required=False)
    }
    logger.debug(request.data)
    args = parser.parse(category_args, request)
    logger.debug(args)
    data = args
    id = data["id"]
    del(data["id"])
    return Category(id).update(data)

@api.route("/category/<category_id>/attribute", methods=["GET"])
@json
def get_category_attribute(category_id):
    return Category(category_id).get_category_attribute_map()

@api.route("/category/<category_id>/attribute", methods=["POST"])
@json
def category_attribute_map(category_id):
    """
        [
            {
                "attribute_id":1,
                "required":1,
                "filter_enabled":1,
                "display_order":2
            }
        ]
    """
    logger.debug(request.data)
    data = ujson.loads(request.data)
    return Category(category_id).update_category_attribute_map(data)


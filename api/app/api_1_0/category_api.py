import logging
from datetime import datetime

from flask import  request
import ujson
from app.api_1_0 import api
from app.decorator import json
from app.src.category import Category

logger = logging.getLogger()

@api.route("/category", methods=["GET"])
@json
def get_category_list():
    result = Category().get_list()
    return result


@api.route("/category/<category_id>", methods=["GET"])
@json
def get_category_by_id(category_id):
    cat = Category(category_id)
    return cat.get()


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
    logger.debug(request.data)
    return Category().create(ujson.loads(request.data))


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
    logger.debug(request.data)
    data = ujson.loads(request.data)
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
                "status_id":1,
                "required":1,
                "filter_enabled":1,
                "display_order":2
            }
        ]
    """
    logger.debug(request.data)
    data = ujson.loads(request.data)
    return Category(category_id).create_category_attribute_map(data)

@api.route("/category/<category_id>/attribute/<attribute_id>", methods=["delete"])
@json
def category_attribute_map_delete(category_id,attribute_id):
    pass


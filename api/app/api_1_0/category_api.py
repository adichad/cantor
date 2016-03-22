import logging
from datetime import datetime

from app.api_1_0 import api
from app.decorator import json
from app.src.category import Category

logger = logging.getLogger()

@api.route("/category", methods=["GET"])
@json
def get_category_list():
    result = Category.get_category_list()
    return result


@api.route("/category/<category_id>", methods=["GET"])
@json
def get_category_by_id(category_id):
    cat = Category(category_id)
    return cat.get_object()


@api.route("/category", methods=["POST"])
@json
def create_category():
    pass


@api.route("/category", methods=["PUT"])
@json
def update_category():
    pass
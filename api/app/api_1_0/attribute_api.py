import logging

from app.api_1_0 import api
from app.decorator import json

logger = logging.getLogger()


@api.route("/attribute", methods=["GET"])
@json
def get_attribute_list():
    pass


@api.route("/attribute/<attribute_id>", methods=["GET"])
@json
def get_attribute_by_id(attribute_id):
    pass


@api.route("/attribute", methods=["POST"])
@json
def create_attribute():
    pass


@api.route("/attribute", methods=["PUT"])
@json
def update_attribute():
    pass



@api.route("/attribute/<attribute_id>/unit", methods=["GET"])
@json
def get_attribute_unit(attribute_id):
    pass

@api.route("/attribute/<attribute_id>/unit", methods=["POST"])
@json
def create_attribute_unit(attribute_id):
    pass

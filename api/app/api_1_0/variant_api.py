import logging
from datetime import datetime

from flask import  request
import ujson
from app.api_1_0 import api
from app.decorator import json
from app.src.variant import Variant

logger = logging.getLogger()

@api.route("/variant/<pageno>/<pagesize>", methods=["GET"])
@json
def get_variant_list(pageno, pagesize):
    result = Variant().get_list()
    return result

@api.route("/variant/<variant_id>", methods=["GET"])
@json
def get_variant_by_id(variant_id):
    var = Variant(variant_id)
    return var.get()

@api.route("/variant", methods=["POST"])
@json
def create_variant():
    """
    list of all multivalued attributes
    {
        "product_id": 1,
        "name":"",
        "description":"",
        "status_id":1,
        "attribute_values": [
            {
                "product_attribute_value_id": 1,
                "status_id": 1
            }
        ]
    }
    :return:
    """
    logger.debug(request.data)
    return Variant().create_variant(ujson.loads(request.data))

@api.route("/variant", methods=["PUT"])
@json
def update_variant():
    logger.debug(request.data)
    data = ujson.loads(request.data)
    id = data["id"]
    del(data["id"])
    return Variant(id).update(data)

@api.route("/variant/<variant_id>/variantsimilar", methods=["GET"])
@json
def get_variantsimilar_list(variant_id):
    var = Variant(variant_id)
    return var.get_similar_variant_list()

@api.route("/variant/<variant_id>/variantsimilar", methods=["POST"])
@json
def add_variantsimilar(variant_id):
    var = Variant(variant_id)
    return var.add_similar_variant(ujson.loads(request.data))

@api.route("/variant/<variant_id>/variantsimilar/<variant_similar_id>", methods=["DELETE"])
@json
def get_variantsimilar_list3(variant_id, variant_similar_id):
    var = Variant(variant_id)
    return var.delete_similar_variant(variant_similar_id)

@api.route("/variant/<variant_id>/variantsimilar/<variant_similar_id>", methods=["PUT"])
@json
def get_variantsimilar_list4(variant_id, variant_similar_id):
    var = Variant(variant_id)
    return var.update_similar_variant(variant_similar_id, ujson.loads(request.data))

import logging
import binascii
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
    pageno = int(pageno)
    pagesize = int(pagesize)

    offset = (pageno-1) * pagesize
    limit = pagesize

    t1=datetime.now()

    variant_list = Variant().get_details_list(limit, offset)
    t2=datetime.now()
    logger.debug((t2-t1).microseconds/1000)
    for variant in variant_list:
        variant['uuid'] = binascii.hexlify(variant['uuid'])

    result = {'total_records':len(variant_list), 'data':variant_list}
    return result

@api.route("/variant/<variant_id>", methods=["GET"])
@json
def get_variant_by_id(variant_id):
    var = Variant(variant_id)
    variant_obj = var.get_details()
    variant_obj['uuid'] = binascii.hexlify(variant_obj['uuid'])
    return variant_obj

# @api.route("/variant", methods=["POST"])
# @json
# def create_variant():
#     """
#     list of all multivalued attributes
#     {
#         "product_id": 1,
#         "name":"",
#         "description":"",
#         "status_id":1,
#         "attribute_values": [
#             {
#                 "product_attribute_value_id": 1,
#                 "status_id": 1
#             }
#         ]
#     }
#     :return:
#     """
#     logger.debug(request.data)
#     return Variant().create_variant(ujson.loads(request.data))

@api.route("/variant", methods=["PUT"])
@json
def update_variant():
    """
    {
        "name":"",
        "description":"",
        "status_id":1,
    }
    """
    logger.debug(request.data)
    data = ujson.loads(request.data)
    id = data["id"]
    del(data["id"])
    return Variant(id).update(data)


@api.route("/variant/<variant_id>/attributevalue", methods=["GET"])
@json
def get_variant_attributevalue(variant_id):
    var = Variant(variant_id)
    return var.get_attribute_values()

# @api.route("/variant/<variant_id>/attributevalue/<attributevalue_id>", methods=["PUT"])
# @json
# def update_variant_attribute_value(variant_id, attributevalue_id):
#     """
#         {
#             "product_attribute_value_id": 1,
#             "status_id": 1
#         }
#     """
#     variant = Variant(variant_id)
#     data = ujson.loads(request.data)
#     return variant.update_attribute_value(attributevalue_id, data)


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

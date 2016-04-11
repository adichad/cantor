import logging
import binascii
from datetime import datetime

from flask import  request
from webargs import fields, validate
from webargs.flaskparser import parser
import ujson
from app.api_1_0 import api
from app.decorator import json
from app.src.product import Product

logger = logging.getLogger()

@api.route("/product/<pageno>/<pagesize>", methods=["GET"])
@json
def get_product_list(pageno, pagesize):
    result = Product().get_list()
    for r in result:
        r['uuid'] = binascii.hexlify(r['uuid'])
    return result

@api.route("/product/<product_id>", methods=["GET"])
@json
def get_product_by_id(product_id):
    product = Product(product_id)
    product_details = product.get()
    product_details['uuid'] = binascii.hexlify(product_details['uuid'])
    return product_details

@api.route("/product", methods=["POST"])
@json
def create_product():
    product_args = {
        "name"          : fields.Str(required=True),
        "description"   : fields.Str(required=True),
        "category_id"   : fields.Int(required=True),
        "status_id"     : fields.Int(required=True),
    }
    logger.debug(request.data)
    args = parser.parse(product_args, request)
    logger.debug(args)
    product = Product().create_product(args)
    product['uuid'] = binascii.hexlify(product['uuid'])
    return product

@api.route("/product", methods=["PUT"])
@json
def update_product():
    logger.debug(request.data)
    data = ujson.loads(request.data)
    id = data["id"]
    del(data["id"])
    prod = Product(id).update(data)
    prod['uuid'] = binascii.hexlify(prod['uuid'])
    return prod


@api.route("/product/<product_id>/attributevalue", methods=["GET"])
@json
def get_product_attribute_value(product_id):
    product = Product(product_id)
    attribute_values = product.get_attribute_values()
    return attribute_values

@api.route("/product/<product_id>/attributevalue", methods=["POST"])
@json
def product_attribute_map(product_id):
    """
        {
            "attribute_id": 3,
            "value":100,
            "unit_id":1,
            "status_id":1
        }
    """
    product = Product(product_id)
    data = ujson.loads(request.data)
    return product.add_attribute_value(data)

@api.route("/product/<product_id>/attributevalue/<attributevalue_id>", methods=["DELETE"])
@json
def delete_product_attribute_value(product_id, attributevalue_id):
    product = Product(product_id)
    return product.delete_attribute_value(attributevalue_id)

@api.route("/product/<product_id>/attributevalue/<attributevalue_id>", methods=["PUT"])
@json
def update_product_attribute_value(product_id, attributevalue_id):
    """
        {
            "value":100,
            "unit_id":1,
            "status_id":1
        }
    """
    product = Product(product_id)
    data = ujson.loads(request.data)
    return product.update_attribute_value(attributevalue_id, data)

# import logging
# from datetime import datetime

# from flask import  request
# import ujson
# from app.api_1_0 import api
# from app.decorator import json
# from app.src.product import Product

# logger = logging.getLogger()



# @api.route("/product/<pageno>/<pagesize>", methods=["GET"])
# @json
# def get_product_list(pageno=1,pagesize=10):
#     result = Product().get_list()
#     return result


# @api.route("/product/<product_id>", methods=["GET"])
# @json
# def get_product_by_id(product_id):
#     cat = Product(product_id)
#     return cat.get()


# @api.route("/product", methods=["POST"])
# @json
# def create_product():
#     logger.debug(request.data)
#     return Product().create(ujson.loads(request.data))


# @api.route("/product", methods=["PUT"])
# @json
# def update_product():
#     logger.debug(request.data)
#     data = ujson.loads(request.data)
#     id = data["id"]
#     del(data["id"])
#     return Product(id).update(data)

# @api.route("/product/<product_id>/attributevalue", methods=["GET"])
# @json
# def get_product_attribute_value(product_id):
#     pass

# @api.route("/product/<product_id>/attributevalue", methods=["POST"])
# @json
# def product_attribute_map(product_id):
#     pass


# @api.route("/product/<product_id>/attributevalue/<attributevalue_id>", methods=["DELETE"])
# @json
# def delete_product_attribute_value(product_id, attributevalue_id):
#     pass


# @api.route("/product/<product_id>/attributevalue/<attributevalue_id>", methods=["PUT"])
# @json
# def update_product_attribute_value(product_id, attributevalue_id):
#     pass

# import logging
# from datetime import datetime

# from flask import  request
# import ujson
# from app.api_1_0 import api
# from app.decorator import json
# #from app.src.category import Category

# logger = logging.getLogger()

# @api.route("/variant/<pageno>/<pagesize>", methods=["GET"])
# @json
# def get_category_list(pageno=1, pagesize=10):
#    pass

# @api.route("/variant/<variant_id>", methods=["GET"])
# @json
# def get_variant_by_id(category_id):
#     pass

# @api.route("/variant", methods=["POST"])
# @json
# def create_variant():
#     """
#     list of all multivalued attributes
#     :return:
#     """
#     pass

# @api.route("/variant", methods=["PUT"])
# @json
# def update_variant():
#     pass

# @api.route("/variant/<variant_id>/variantsimilar", methods=["GET"])
# @json
# def get_variantsimilar_list(variant_id):
#    pass

# @api.route("/variant/<variant_id>/variantsimilar", methods=["POST"])
# @json
# def get_variantsimilar_list(variant_id):
#    pass

# @api.route("/variant/<variant_id>/variantsimilar/<variantsimilarid>", methods=["DELETE"])
# @json
# def get_variantsimilar_list(variant_id):
#    pass

# @api.route("/variant/<variant_id>/variantsimilar/<variantsimilarid>", methods=["PUT"])
# @json
# def get_variantsimilar_list(variant_id):
#    pass

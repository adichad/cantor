# import logging
# from datetime import datetime

# from flask import  request
# import ujson
# from app.api_1_0 import api
# from app.decorator import json
# from app.src.subscription import Subscription

# logger = logging.getLogger()

# @api.route("/subscription/<pageno>/<pagesize>", methods=["GET"])
# @json
# def get_subscription_list(pageno=1,pagesize=10):
#     result = Subscription().get_list()
#     return result


# @api.route("/subscription/<subscription_id>", methods=["GET"])
# @json
# def get_subscription_by_id(subscription_id):
#     cat = Subscription(subscription_id)
#     return cat.get()


# @api.route("/subscription", methods=["POST"])
# @json
# def create_subscription():
#     logger.debug(request.data)
#     return Subscription().create(ujson.loads(request.data))


# @api.route("/subscription", methods=["PUT"])
# @json
# def update_subscription():
#     logger.debug(request.data)
#     data = ujson.loads(request.data)
#     id = data["id"]
#     del(data["id"])
#     return Subscription(id).update(data)


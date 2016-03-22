import logging
from datetime import datetime

from app.api_1_0 import api
from app.decorator import json

logger = logging.getLogger()

@api.route("/catetory", methods=["GET"])
@json
def get_category_list():
    pass


@api.route("/catetory/<category_id>", methods=["GET"])
@json
def get_category_by_id():
    pass


@api.route("/catetory", methods=["POST"])
@json
def create_category():
    pass


@api.route("/catetory", methods=["PUT"])
@json
def update_category():
    pass
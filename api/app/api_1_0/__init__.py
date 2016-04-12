__author__ = "cantor"

from flask import Blueprint

api = Blueprint("api", __name__)
from app.api_1_0 import attribute_api, catalog_api, category_api, product_api, subscription_api, variant_api, offer_api, combo_api, errors

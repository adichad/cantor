import logging
from datetime import datetime

from app.api_1_0 import api
from app.decorator import json

logger = logging.getLogger()

@api.route("/time", methods=["GET"])
@json
def get_time():
    return {'time':datetime.now()}

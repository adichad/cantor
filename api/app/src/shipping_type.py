import uuid
import binascii
import logging
from sqlalchemydb import AlchemyDB
from base_catalog import BaseCatalog

logger = logging.getLogger()

class ShippingType(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "shipping_type", id)
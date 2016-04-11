import uuid
import binascii
import logging
from sqlalchemydb import AlchemyDB
from base_catalog import BaseCatalog

logger = logging.getLogger()


class Subscription(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "subscription", id)

    def create_subscription(self, subscription_data):
        self.uuid = uuid.uuid1().hex
        subscription_data['uuid'] = binascii.unhexlify(self.uuid)
        db = AlchemyDB()
        self.id = db.insert_row(self.table, **subscription_data)
        return self.get()

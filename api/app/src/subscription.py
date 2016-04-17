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
        uuid_entity_ref_data = {
            'uuid'          : binascii.unhexlify(self.uuid),
            'entity_id'     : self.id,
            'entity_type'   : "subscription"
        }
        db.insert_row("uuid_entity_ref", **uuid_entity_ref_data)
        return self.get()

    def get_conditions(self):
        conditions = []
        db = AlchemyDB()
        mappings = db.select_outer_join(["subscription_condition", "condition"], [{"condition_id": "id"}], [({"subscription_condition.subscription_id": self.id},)])
        logger.debug(mappings)
        for m in mappings:
            logger.debug(m)
        return conditions

    def attach_condition(self, condition_data):
        db = AlchemyDB()
        condition_data['subscription_id'] = self.id
        db.insert_row("subscription_condition", **condition_data)
        return self.get_conditions()


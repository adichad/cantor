import uuid
import binascii
import logging
from sqlalchemydb import AlchemyDB
from base_catalog import BaseCatalog
from variant import Variant

logger = logging.getLogger()


class Subscription(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "subscription", id)

    def get_details(self):
        subscription_details = self.get()
        variant_obj = Variant(subscription_details['variant_id'])
        subscription_details['variant'] = variant_obj.get_details()
        return subscription_details

    def get_detailed_list(self, limit, offset):
        db = AlchemyDB()

        result = db.find(self.table, _limit=limit, _offset=offset)
        total_results = db.count_rows(self.table)

        status_dict = self.get_status_dict(db)
        for r in result:
            variant_obj = Variant(r['variant_id'])
            r['variant'] = variant_obj.get_details()
            r["status"] = status_dict[r['status_id']]
        return result, total_results

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
        status_dict = self.get_status_dict(db)
        mappings = db.select_outer_join(["subscription_condition", "condition"], [{"condition_id": "id"}], [({"subscription_condition.subscription_id": self.id},)])
        logger.debug(mappings)
        for m in mappings:
            conditions.append({'id':m['condition_id'], 'name':m['condition_name'], 'description':m['condition_description'], 'status_id':m['subscription_condition_status_id'], 'status':status_dict[m['subscription_condition_status_id']]})
        return conditions

    def attach_condition(self, condition_data):
        db = AlchemyDB()
        condition_data['subscription_id'] = self.id
        db.insert_row("subscription_condition", **condition_data)
        return self.get_conditions()


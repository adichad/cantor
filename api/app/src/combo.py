import uuid
import binascii
import logging
import itertools
from sqlalchemydb import AlchemyDB
from base_catalog import BaseCatalog

logger = logging.getLogger()


class Combo(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "combo", id)

    def create_combo(self, combo_args):
        self.uuid = uuid.uuid1().hex
        db = AlchemyDB()
        combo_data = {
            'uuid'          : binascii.unhexlify(self.uuid),
            'name'          : combo_args['name'],
            'description'   : combo_args['description'],
            'status_id'     : combo_args['status_id']
        }
        self.id = db.insert_row(self.table, **combo_data)
        entity_combo_args = []
        for entity in combo_args['entities']:
            entity_combo_args.append({
                'combo_id'      : self.id,
                'entity_id'     : entity['entity_id'],
                'entity_type'   : entity['entity_type'],
                'quantity'      : entity['quantity'],
                'status_id'     : combo_args['status_id']
            })
        db.insert_row_batch("entity_combo", entity_combo_args)
        uuid_entity_ref_data = {
            'uuid'          : binascii.unhexlify(self.uuid),
            'entity_id'     : self.id,
            'entity_type'   : "combo"
        }
        db.insert_row("uuid_entity_ref", **uuid_entity_ref_data)
        return self.get()
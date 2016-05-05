import logging
from base_catalog import BaseCatalog
from sqlalchemydb import AlchemyDB

logger = logging.getLogger()


class StoreFront(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "store_front", id)

    def get_store_front_id_entity_map(self):
        db = AlchemyDB()
        db_list = db.find("store_front_entity", store_front_id=self.id)
        status_dict = self.get_status_dict(db)
        for item in db_list:
            item['status'] = status_dict[item['status_id']]
        return db_list

    def update_store_front_id_entity_map(self, data):
        db = AlchemyDB()
        
        ENABLED = 1
        DELETED = 3

        current = []
        new_data_store = {}
        for d in data:
            current.append(d['entity_type']+"_"+str(d['entity_id']))
            new_data_store[d['entity_type']+"_"+str(d['entity_id'])] = d

        existing_mappings = db.find('store_front_entity', store_front_id=self.id)
        enabled = []
        deleted = []
        old_data_store = {}
        for mapping in existing_mappings:
            if mapping['status_id'] == ENABLED:
                enabled.append(mapping['entity_type']+"_"+str(mapping['entity_id']))
            elif mapping['status_id'] == DELETED:
                deleted.append(mapping['entity_type']+"_"+str(mapping['entity_id']))
            old_data_store[mapping['entity_type']+"_"+str(mapping['entity_id'])] = mapping


        to_be_inserted, to_be_marked_enabled, to_be_marked_deleted = self.resolve_ops(current, enabled, deleted)

        logger.debug(current)
        logger.debug(enabled)
        logger.debug(deleted)
        logger.debug("---------")
        logger.debug(to_be_inserted)
        logger.debug(to_be_marked_enabled)
        logger.debug(to_be_marked_deleted)

        insert = []
        update = []

        for data in to_be_inserted:
            insert.append({
                    "store_front_id"    : self.id,
                    "entity_type"       : new_data_store[data]["entity_type"],
                    "entity_id"         : new_data_store[data]["entity_id"],
                    "display_order"     : new_data_store[data]["display_order"],
                    "status_id"         : ENABLED
                })

        for data in to_be_marked_enabled:
            update.append({
                    "store_front_id"    : self.id,
                    "entity_type"       : new_data_store[data]["entity_type"],
                    "entity_id"         : new_data_store[data]["entity_id"],
                    "display_order"     : new_data_store[data]["display_order"],
                    "status_id"         : ENABLED
                })
        for data in to_be_marked_deleted:
            update.append({
                    "store_front_id"    : self.id,
                    "entity_type"       : old_data_store[data]["entity_type"],
                    "entity_id"         : old_data_store[data]["entity_id"],
                    "display_order"     : old_data_store[data]["display_order"],
                    "status_id"         : DELETED
                })

        logger.debug(insert)
        if len(insert):
            db.insert_row_batch('store_front_entity', insert)

        logger.debug(update)
        if len(update):
            for item in update:
                db.update_row_new("store_front_entity", 
                    where={
                        "store_front_id": item["store_front_id"],
                        "entity_type"   : item["entity_type"],
                        "entity_id"     : item["entity_id"]}, 
                    val={
                        "display_order" : item["display_order"],
                        "status_id"     : item["status_id"]})

        return self.get_store_front_id_entity_map()


import logging
from base_catalog import BaseCatalog
from sqlalchemydb import AlchemyDB
logger = logging.getLogger()


class Attribute(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "attribute", id)

    def get_unit(self):
        db = AlchemyDB()
        result = db.find('attribute_unit', attribute_id=self.id)
        status_dict = self.get_status_dict()
        for r in result:
            r["status"] = status_dict[r["status_id"]]
        return result

    def update_unit_map(self, unit_list):
        db = AlchemyDB()

        ENABLED = 1
        DELETED = 3

        existing_mappings = db.find('attribute_unit', attribute_id=self.id)
        enabled = []
        deleted = []
        for mapping in existing_mappings:
            if mapping['status_id'] == ENABLED:
                enabled.append(mapping['unit_id'])
            elif mapping['status_id'] == DELETED:
                deleted.append(mapping['unit_id'])

        to_be_inserted, to_be_marked_enabled, to_be_marked_deleted = self.resolve_ops(unit_list, enabled, deleted)

        logger.debug(to_be_inserted)
        logger.debug(to_be_marked_enabled)
        logger.debug(to_be_marked_deleted)

        insert = []
        update = []

        for unit_id in to_be_inserted:
            insert.append({
                    "attribute_id"  : self.id,
                    "unit_id"       : unit_id,
                    "status_id"     : ENABLED
                })

        for unit_id in to_be_marked_enabled:
            update.append({
                    "attribute_id"  : self.id,
                    "unit_id"       : unit_id,
                    "status_id"     : ENABLED
                })
        for unit_id in to_be_marked_deleted:
            update.append({
                    "attribute_id"  : self.id,
                    "unit_id"       : unit_id,
                    "status_id"     : DELETED
                })

        if len(insert):
            db.insert_row_batch('attribute_unit', insert)

        if len(update):
            for item in update:
                db.update_row_new("attribute_unit", where={"attribute_id": item["attribute_id"], "unit_id":item["unit_id"]}, val={"status_id":item["status_id"]})

        return self.get_unit()


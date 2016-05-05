import logging
from base_catalog import BaseCatalog
from sqlalchemydb import AlchemyDB

logger = logging.getLogger()


class Category(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "category", id)

    def update_category_attribute_map(self, data):
        db = AlchemyDB()
        
        ENABLED = 1
        DELETED = 3

        current = []
        new_data_store = {}
        for d in data:
            current.append(d['attribute_id'])
            new_data_store[d['attribute_id']] = d

        existing_mappings = db.find('category_attribute', category_id=self.id)
        enabled = []
        deleted = []
        old_data_store = {}
        for mapping in existing_mappings:
            if mapping['status_id'] == ENABLED:
                enabled.append(mapping['attribute_id'])
            elif mapping['status_id'] == DELETED:
                deleted.append(mapping['attribute_id'])
            old_data_store[mapping['attribute_id']] = mapping


        to_be_inserted, to_be_marked_enabled, to_be_marked_deleted = self.resolve_ops(current, enabled, deleted)

        insert = []
        update = []

        for attribute_id in to_be_inserted:
            insert.append({
                    "category_id"   : self.id,
                    "attribute_id"  : attribute_id,
                    "required"      : new_data_store[attribute_id]["required"],
                    "filter_enabled": new_data_store[attribute_id]["filter_enabled"],
                    "display_order" : new_data_store[attribute_id]["display_order"],
                    "status_id"     : ENABLED
                })

        for attribute_id in to_be_marked_enabled:
            update.append({
                    "category_id"   : self.id,
                    "attribute_id"  : attribute_id,
                    "required"      : new_data_store[attribute_id]["required"],
                    "filter_enabled": new_data_store[attribute_id]["filter_enabled"],
                    "display_order" : new_data_store[attribute_id]["display_order"],
                    "status_id"     : ENABLED
                })
        for attribute_id in to_be_marked_deleted:
            update.append({
                    "category_id"   : self.id,
                    "attribute_id"  : attribute_id,
                    "required"      : old_data_store[attribute_id]["required"],
                    "filter_enabled": old_data_store[attribute_id]["filter_enabled"],
                    "display_order" : old_data_store[attribute_id]["display_order"],
                    "status_id"     : DELETED
                })

        logger.debug(insert)
        if len(insert):
            db.insert_row_batch('category_attribute', insert)

        logger.debug(update)
        if len(update):
            for item in update:
                db.update_row_new("category_attribute", 
                    where={
                        "category_id": item["category_id"],
                        "attribute_id":item["attribute_id"]}, 
                    val={
                        "required":item["required"],
                        "filter_enabled":item["filter_enabled"],
                        "display_order":item["display_order"],
                        "status_id":item["status_id"]})

        return self.get_category_attribute_map()

    def get_category_attribute_map(self):
        db = AlchemyDB()
        mappings = db.select_outer_join(["category_attribute", "attribute"], [{"attribute_id": "id"}], [({"category_attribute.category_id": self.id},)])
        for mapping in mappings:
            attribute_id = mapping['attribute_id']
            unit_mappings = db.select_outer_join(["attribute_unit", "unit"], [{"unit_id": "id"}], [({"attribute_unit.attribute_id": attribute_id},)])
            units = []
            for unit_mapping in unit_mappings:
                units.append({"id":unit_mapping["unit_id"],"name":unit_mapping["unit_name"], "status_id":unit_mapping["unit_status_id"]})
            mapping["units"] = units
        mappings.sort(key=lambda m: m['category_attribute_display_order'])
        return mappings



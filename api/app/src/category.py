import logging
from base_catalog import BaseCatalog
from sqlalchemydb import AlchemyDB

logger = logging.getLogger()


class Category(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "category", id)

    def create_category_attribute_map(self, data):
        db = AlchemyDB()
        insert = []
        for item in data:
            existing_mappings = db.find('category_attribute', category_id=self.id, attribute_id=item["attribute_id"])
            if len(existing_mappings) == 0:
                item["category_id"] = self.id
                insert.append(item)
        if len(insert):
            db.insert_row_batch('category_attribute', insert)
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
        return mappings



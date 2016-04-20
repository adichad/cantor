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
        return result

    def add_unit_map(self, unit_list):
        db = AlchemyDB()

        insert = []
        for item in unit_list:
            existing_mappings = db.find('attribute_unit', attribute_id=self.id, unit_id=item["unit_id"])
            if len(existing_mappings) == 0:
                item["attribute_id"] = self.id
                insert.append(item)

        if len(insert):
            db.insert_row_batch('attribute_unit', insert)
        return self.get_unit()
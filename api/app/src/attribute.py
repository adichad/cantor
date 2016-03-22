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
            item["attribute_id"] = self.id
            insert.append(item)

        db.insert_row_batch('attribute_unit', insert)
        return self.get_unit()
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
            item["category_id"] = self.id
            insert.append(item)
        db.insert_row_batch('category_attribute', insert)
        return self.get_category_attribute_map()

    def get_category_attribute_map(self):
        db = AlchemyDB()
        data = db.find('category_attribute', category_id=self.id)
        return data



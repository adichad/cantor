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
        return mappings



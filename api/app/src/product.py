import logging
from sqlalchemydb import AlchemyDB
from base_catalog import BaseCatalog

logger = logging.getLogger()


class Product(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "product", id)

    def get_attribute_values(self):
        db = AlchemyDB()
        product_attribute_values = db.find("product_attribute_value", product_id=self.id)
        logger.debug(product_attribute_values)
        attribute_ids = list(set([pav['attribute_id'] for pav in product_attribute_values]))
        attributes = db.find("attribute", id=attribute_ids)
        attribute_store = {at['id']:at for at in attributes}
        logger.debug(attribute_store)
        for pav in product_attribute_values:
            pav['attribute'] = attribute_store[pav['attribute_id']]
            pav['value'] = db.find_one(pav['attribute']['value_type']+'_value', id=pav['value_id'])
        return product_attribute_values


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

        product_attribute_value_ids = [pav['id'] for pav in product_attribute_values]
        logger.debug(product_attribute_value_ids)

        product_attribute_value_units = db.find("product_attribute_value_unit", order_by="product_attribute_value_id", product_attribute_value_id=product_attribute_value_ids)
        logger.debug(product_attribute_value_units)

        product_attribute_value_unit_ids = [ o['unit_id'] for o in product_attribute_value_units]
        product_attribute_value_unit_store = {pvu['product_attribute_value_id']:pvu for pvu in product_attribute_value_units}

        units = db.find("unit", id=product_attribute_value_unit_ids)
        unit_store = {u['id']:u for u in units}

        for pav in product_attribute_values:
            pav['attribute'] = attribute_store[pav['attribute_id']]
            pav['value'] = db.find_one(pav['attribute']['value_type']+'_value', id=pav['value_id'])
            pav['value_unit'] = unit_store.get(product_attribute_value_unit_store.get(pav['id'],{}).get('unit_id',-1))
        return product_attribute_values

    def add_attribute_value(self, attribute_value):
        db = AlchemyDB()
        attribute_id = attribute_value['attribute_id']
        attribute = db.find_one("attribute", id=attribute_id)

        value_data = {
            "value":    attribute_value['value'], 
            "status_id":attribute_value['status_id']
        }
        value_id = db.insert_row(attribute['value_type']+'_value', **value_data)

        product_attribute_value_data = {
            "product_id":   self.id,
            "attribute_id": attribute_id,
            "value_id":     value_id,
            "status_id":    attribute_value['status_id']
        }
        product_attribute_value_id = db.insert_row("product_attribute_value", **product_attribute_value_data)

        product_attribute_value_unit_data = {
            "product_attribute_value_id":   product_attribute_value_id,
            "unit_id":                      attribute_value['status_id'],
            "status_id":                    attribute_value['status_id']
        }
        product_attribute_value_unit_id = db.insert_row("product_attribute_value_unit", **product_attribute_value_unit_data)

        return True
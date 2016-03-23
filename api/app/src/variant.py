import logging
from sqlalchemydb import AlchemyDB
from base_catalog import BaseCatalog

logger = logging.getLogger()


class Variant(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "variant", id)

    def get_similar_variant_list(self):
        db = AlchemyDB()
        similar_variants = db.find("variant_similar", variant_id=self.id)
        logger.debug(similar_variants)
        return similar_variants

    def add_similar_variant(self, similar_variant):
        similar_variant['variant_id'] = self.id
        db = AlchemyDB()
        similar_variant_id = db.insert_row("variant_similar", **similar_variant)
        return similar_variant_id

    def delete_similar_variant(self, variant_similar_id):
        db = AlchemyDB()
        db.delete_row("variant_similar", variant_id=self.id, id=variant_similar_id)
        return True

    def update_similar_variant(self, variant_similar_id, similar_variant):
        db = AlchemyDB()
        db.update_row_new("variant_similar", where={"variant_id": self.id, "id":variant_similar_id}, val=similar_variant)
        return True

    def create_variant(self, payload):
        db = AlchemyDB()
        variant_data = {
            "product_id":   payload['product_id'],
            "name":         payload['name'],
            "description":  payload['description'],
            "status_id":    payload['status_id']
        }

        self.id = db.insert_row("variant", **variant_data)

        variant_product_attribute_value_data = []
        for av in payload['attribute_values']:
            variant_product_attribute_value_data.append({
                "variant_id": self.id,
                "product_attribute_value_id": av['product_attribute_value_id'],
                "status_id": av['status_id']
            })
        db.insert_row_batch("variant_product_attribute_value", variant_product_attribute_value_data)
        return True


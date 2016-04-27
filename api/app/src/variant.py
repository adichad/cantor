import logging
from sqlalchemydb import AlchemyDB
from base_catalog import BaseCatalog

logger = logging.getLogger()


class Variant(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "variant", id)

    def get_details_list(self):
        db = AlchemyDB()
        result = db.find(self.table)
        status_dict = self.get_status_dict(db)
        logger.debug(result)
        logger.debug(status_dict)
        for r in result:
            r["status"] = status_dict[r['status_id']]
            product = db.find_one("product", id=r["product_id"])
            r["product_name"] = product["name"]
        return result

    def get_details(self):
        db = AlchemyDB()
        result = db.find_one(self.table, id=self.id)
        status_dict = self.get_status_dict(db)
        logger.debug(result)
        product = db.find_one("product", id=result["product_id"])
        result["product_name"] = product["name"]
        result["status"] = status_dict[result["status_id"]]
        return result

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

    def get_attribute_values(self):
        db = AlchemyDB()

        variant_product_attribute_values = db.find("variant_product_attribute_value", variant_id=self.id)
        product_attribute_value_ids = [vpav['product_attribute_value_id'] for vpav in variant_product_attribute_values]

        product_attribute_values = db.find("product_attribute_value", id=product_attribute_value_ids)
        logger.debug(product_attribute_values)

        attribute_ids = list(set([pav['attribute_id'] for pav in product_attribute_values]))
        attributes = db.find("attribute", id=attribute_ids)
        attribute_store = {at['id']:at for at in attributes}
        logger.debug(attribute_store)

        product_attribute_value_ids = [pav['id'] for pav in product_attribute_values]
        logger.debug(product_attribute_value_ids)

        product_attribute_value_units = db.find("product_attribute_value_unit", order_by="product_attribute_value_id", product_attribute_value_id=product_attribute_value_ids)
        logger.debug(product_attribute_value_units)

        product_attribute_value_unit_ids = [o['unit_id'] for o in product_attribute_value_units]
        product_attribute_value_unit_store = {pvu['product_attribute_value_id']:pvu for pvu in product_attribute_value_units}

        units = db.find("unit", id=product_attribute_value_unit_ids)
        unit_store = {u['id']:u for u in units}

        product_attribute_value_store = {}
        for pav in product_attribute_values:
            pav['attribute'] = attribute_store[pav['attribute_id']]
            pav['value'] = db.find_one('value_'+pav['attribute']['value_type'], id=pav['value_id'])
            pav['value_unit'] = unit_store.get(product_attribute_value_unit_store.get(pav['id'],{}).get('unit_id',-1))
            product_attribute_value_store[pav['id']] = pav
        for o in variant_product_attribute_values:
            o['attribute_value'] = product_attribute_value_store[o['product_attribute_value_id']]
        return variant_product_attribute_values

    def update_attribute_value(self, attributevalue_id, data):
        db = AlchemyDB()
        db.update_row_new("variant_product_attribute_value", where={"variant_id": self.id, "id":attributevalue_id}, val=data)
        return True


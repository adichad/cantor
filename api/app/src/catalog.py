import logging
import binascii
from sqlalchemydb import AlchemyDB
logger = logging.getLogger()


class Catalog():

    @staticmethod
    def search(uuid):
        db = AlchemyDB()
        entity_ref = db.find_one("uuid_entity_ref", uuid=binascii.unhexlify(uuid))
        if entity_ref:
            if entity_ref['entity_type'] == 'combo':
                return Catalog.get_combo(entity_ref['entity_id'], db)
            elif entity_ref['entity_type'] == 'product':
                return Catalog.get_product(entity_ref['entity_id'], db)
            elif entity_ref['entity_type'] == 'variant':
                return Catalog.get_variant(entity_ref['entity_id'], db)
            elif entity_ref['entity_type'] == 'subscription':
                return Catalog.get_subscription(entity_ref['entity_id'], db)
        return {}

    @staticmethod
    def get_combo(id, db):
        combo_row = db.find_one("combo", id=id)
        products = []

        combo_entities = db.find("entity_combo", combo_id=id)
        for entity in combo_entities:
            if entity['entity_type'] == 'product':
                db_product = db.find_one("product", id=entity['entity_id'])

                # category
                db_category = db.find_one("category", id=db_product['category_id'])
                category = {
                    "id"            : db_category['id'],
                    "name"          : db_category['name'],
                    "description"   : db_category['description'],
                    "parent_id"     : db_category['parent_id']
                }

                # parent_categories
                parent_id = db_category['parent_id']
                parent_categories = []
                while parent_id != 0:
                    db_parent_category = db.find_one("category", id=parent_id)
                    parent_category = {
                        "id"            : db_parent_category['id'],
                        "name"          : db_parent_category['name'],
                        "description"   : db_parent_category['description'],
                        "parent_id"     : db_parent_category['parent_id']
                    }
                    parent_categories.append(parent_category)
                    parent_id = db_parent_category['parent_id']

                # attributes
                attributes = []
                product_attribute_values = db.find("product_attribute_value", product_id=entity['entity_id'])
                attribute_ids = [pav['attribute_id'] for pav in product_attribute_values]
                db_attributes = db.find("attribute", id=attribute_ids)
                db_attribute_store = {}
                pav_store = {}
                for attr in db_attributes:
                    db_attribute_store[attr['id']] = attr
                for pav in product_attribute_values:
                    db_value = db.find_one('value_'+db_attribute_store[pav['attribute_id']]['value_type'], id=pav['value_id'])
                    attribute = {
                        "id": pav['attribute_id'],
                        "name": db_attribute_store[pav['attribute_id']]['name'],
                        "description": db_attribute_store[pav['attribute_id']]['description'],
                        "value_type": db_attribute_store[pav['attribute_id']]['value_type'],
                        "value": db_value['value']
                    }
                    attributes.append(attribute)
                    pav_store[pav['id']] = attribute

                # variants
                db_variants = db.find("variant", product_id=entity['entity_id'])
                db_variant_ids = [v['id'] for v in db_variants]
                db_subscriptions = db.find("subscription", variant_id=db_variant_ids)
                variants = []
                for v in db_variants:
                    va = []
                    db_vpavs = db.find("variant_product_attribute_value", variant_id=v['id'])
                    for vpav in db_vpavs:
                        va.append(pav_store[vpav['product_attribute_value_id']])
                    subscriptions = []
                    for s in db_subscriptions:
                        subscription = {
                            "uuid"                  : binascii.hexlify(s['uuid']),
                            "available_quantity"    : s['quantity_available'],
                            "seller_indicated_price": s['seller_indicated_price'],
                            "valid_from"            : s['valid_from'],
                            "valid_thru"            : s["valid_thru"]
                        }
                        subscriptions.append(subscription)
                    variant = {
                        "uuid"                  : binascii.hexlify(v['uuid']),
                        "name"                  : v['name'],
                        "description"           : v['description'],
                        "variant_attributes"    : va,
                        "subscriptions"         : subscriptions
                    }
                    variants.append(variant)
                product = {
                    "uuid"              : binascii.hexlify(db_product['uuid']),
                    "name"              : db_product['name'],
                    "description"       : db_product['description'],
                    "category"          : category,
                    "parent_categories" : parent_categories,
                    "attributes"        : attributes,
                    "variants"          : variants
                }
                products.append(product)

        db_offers = db.find("offer", entity_id=id, entity_type='combo')
        offers = []
        for db_offer in db_offers:
            offer = {
                "id"                    : db_offer['id'],
                "discount_percent"      : db_offer['discount_percent'],
                "discount_cap_amount"   : db_offer['discount_cap_amount'],
                "valid_from"            : db_offer['valid_from'],
                "valid_thru"            : db_offer['valid_thru']
            }
            offers.append(offer)

        return {
            'combo':{
                'uuid'          : binascii.hexlify(combo_row['uuid']),
                'name'          : combo_row['name'],
                'description'   : combo_row['description'],
                'offers'        : offers,
                'products'      : products
            }
        }

    @staticmethod
    def get_product(id):
        pass

    @staticmethod
    def get_variant(id):
        pass

    @staticmethod
    def get_subscription(uuid):
        pass
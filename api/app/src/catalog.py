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
                category, parent_categories = Catalog.get_category(db_product['category_id'], db)
                # attributes
                attributes, pav_store = Catalog.get_product_attribute_values(entity['entity_id'], db)
                # variants
                variants = Catalog.get_variants(entity['entity_id'], pav_store, db)
                # product
                product = {
                    "uuid"              : binascii.hexlify(db_product['uuid']),
                    "name"              : db_product['name'],
                    "description"       : db_product['description'],
                    "category"          : category,
                    "parent_categories" : parent_categories,
                    "attributes"        : attributes,
                    "variants"          : variants,
                    "media"             : []
                }
                products.append(product)
            elif entity['entity_type'] == 'variant':
                db_variant = db.find_one("variant", id=entity['entity_id'])
                # product
                db_product = db.find_one("product", id=db_variant['product_id'])
                # category
                category, parent_categories = Catalog.get_category(db_product['category_id'], db)
                # attributes
                attributes, pav_store = Catalog.get_product_attribute_values(db_variant['product_id'], db)
                # variants
                variant = Catalog.populate_variant(db_variant, pav_store, db)
                # product
                product = {
                    "uuid"              : binascii.hexlify(db_product['uuid']),
                    "name"              : db_product['name'],
                    "description"       : db_product['description'],
                    "category"          : category,
                    "parent_categories" : parent_categories,
                    "attributes"        : attributes,
                    "variants"          : [variant,],
                    "media"             : []
                }
                products.append(product)
            elif entity['entity_type'] == 'subscription':
                db_subscription = db.find_one("subscription", id=entity['entity_id'])
                subscription = Catalog.populate_subscription(db_subscription, db)
                db_variant = db.find_one("variant", id=db_subscription['variant_id'])
                # product
                db_product = db.find_one("product", id=db_variant['product_id'])
                # category
                category, parent_categories = Catalog.get_category(db_product['category_id'], db)
                # attributes
                attributes, pav_store = Catalog.get_product_attribute_values(db_variant['product_id'], db)
                # variants
                variant = Catalog.populate_variant(db_variant, pav_store, db, populate_subscriptions=False)
                variant['subscriptions'] = [subscription, ]
                # product
                product = {
                    "uuid"              : binascii.hexlify(db_product['uuid']),
                    "name"              : db_product['name'],
                    "description"       : db_product['description'],
                    "category"          : category,
                    "parent_categories" : parent_categories,
                    "attributes"        : attributes,
                    "variants"          : [variant,],
                    "media"             : []
                }
                products.append(product)

        offers = Catalog.get_offers_by_entity('combo', id, db)

        return {
            'combo':{
                'uuid'          : binascii.hexlify(combo_row['uuid']),
                'name'          : combo_row['name'],
                'description'   : combo_row['description'],
                'offers'        : offers,
                'products'      : products,
                'media'         : []
            }
        }

    @staticmethod
    def get_product(id, db):
        pass

    @staticmethod
    def get_variant(id, db):
        pass

    @staticmethod
    def get_subscription(id, db):
        pass


    @staticmethod
    def get_category(category_id, db):
        db_category = db.find_one("category", id=category_id)
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

        return category, parent_categories

    @staticmethod
    def get_offers_by_entity(entity_type, entity_id, db):
        db_offers = db.find("offer", entity_id=entity_id, entity_type=entity_type)
        offers = []
        for db_offer in db_offers:
            offer = {
                "id"                    : db_offer['id'],
                "discount_percent"      : db_offer['discount_percent'],
                "discount_cap_amount"   : db_offer['discount_cap_amount'],
                "valid_from"            : db_offer['valid_from'],
                "valid_thru"            : db_offer['valid_thru'],
                "media"                 : []
            }
            offers.append(offer)
        return offers

    @staticmethod
    def get_product_attribute_values(product_id, db):
        attributes = []
        product_attribute_values = db.find("product_attribute_value", product_id=product_id)
        attribute_ids = [pav['attribute_id'] for pav in product_attribute_values]
        db_attributes = db.find("attribute", id=attribute_ids)
        db_attribute_store = {}
        pav_store = {}
        for attr in db_attributes:
            db_attribute_store[attr['id']] = attr
        for pav in product_attribute_values:
            db_value = db.find_one('value_'+db_attribute_store[pav['attribute_id']]['value_type'], id=pav['value_id'])
            attribute = {
                "id"            : pav['attribute_id'],
                "name"          : db_attribute_store[pav['attribute_id']]['name'],
                "description"   : db_attribute_store[pav['attribute_id']]['description'],
                "value_type"    : db_attribute_store[pav['attribute_id']]['value_type'],
                "value"         : db_value['value'],
                "media"         : []
            }
            attributes.append(attribute)
            pav_store[pav['id']] = attribute
        return attributes, pav_store

    @staticmethod
    def get_variants(product_id, pav_store, db):
        db_variants = db.find("variant", product_id=product_id)
        variants = []
        for db_variant in db_variants:
            variant = Catalog.populate_variant(db_variant, pav_store, db)
            variants.append(variant)
        return variants

    @staticmethod
    def populate_variant(variant, pav_store, db, populate_subscriptions=True):
        variant_attributes = []
        db_vpavs = db.find("variant_product_attribute_value", variant_id=variant['id'])
        for vpav in db_vpavs:
            variant_attributes.append(pav_store[vpav['product_attribute_value_id']])
        subscriptions = []
        if populate_subscriptions:
            db_subscriptions = db.find("subscription", variant_id=variant['id'])
            for s in db_subscriptions:
                subscription = Catalog.populate_subscription(s, db)
                subscriptions.append(subscription)
        variant = {
            "uuid"                  : binascii.hexlify(variant['uuid']),
            "name"                  : variant['name'],
            "description"           : variant['description'],
            "variant_attributes"    : variant_attributes,
            "subscriptions"         : subscriptions
        }
        return variant

    @staticmethod
    def populate_subscription(subscription, db):
        db_seller = db.find_one("seller", id=subscription['seller_id'])
        seller = {
            "id"            : db_seller['id'],
            "name"          : db_seller['name'],
            "address"       : db_seller['address'],
            "email"         : db_seller['email'],
            "voice_contact" : db_seller['voice_contact']
        }
        subscription = {
            "uuid"                  : binascii.hexlify(subscription['uuid']),
            "available_quantity"    : subscription['quantity_available'],
            "seller_indicated_price": subscription['seller_indicated_price'],
            "valid_from"            : subscription['valid_from'],
            "valid_thru"            : subscription["valid_thru"],
            "seller"                : seller
        }
        return subscription


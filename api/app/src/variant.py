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


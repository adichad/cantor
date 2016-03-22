import logging
from base_catalog import BaseCatalog

logger = logging.getLogger()


class Category(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "category", id)

    def category_attribute_map(self, attribute_id_list):
        pass




from sqlalchemydb import AlchemyDB

import logging

logger = logging.getLogger()


class BaseCatalog:

    def __init__(self, table, id=None):
        self.table = table
        self.id = id

    def get(self):
        db = AlchemyDB()
        result = db.find_one(self.table, id=self.id)
        logger.debug(result)
        return result

    def get_list(self):
        db = AlchemyDB()
        result = db.find(self.table)
        logger.debug(result)
        return result

    def create(self, args):
        db = AlchemyDB()
        id = db.insert_row(self.table, **args)
        return id

    def update(self, args):
        db = AlchemyDB()
        result = db.update_row_new(self.table, id=self.id, **args)
        return result


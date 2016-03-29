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
        self.id = db.insert_row(self.table, **args)
        return self.get()

    def update(self, args):
        db = AlchemyDB()
        db.update_row_new(self.table, where={"id": self.id}, val=args)
        return self.get()


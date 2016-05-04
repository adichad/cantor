import logging
from base_catalog import BaseCatalog
from sqlalchemydb import AlchemyDB
logger = logging.getLogger()


class Unit(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "unit", id)

    def create_unit(self, args):
        db = AlchemyDB()
        existing_unit = db.find_one(self.table, name=args['name'])
        if existing_unit:
            return {"message":"Unit with same name already exists", "success":False}
        self.id = db.insert_row(self.table, **args)
        return self.get()

    def update_unit(self, args):
        db = AlchemyDB()
        existing_unit = db.find_one(self.table, name=args['name'])
        if existing_unit:
            return {"message":"Unit with same name already exists", "success":False}
        db.update_row_new(self.table, where={"id": self.id}, val=args)
        return self.get()


class Status(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "status", id)
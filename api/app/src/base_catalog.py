from sqlalchemydb import AlchemyDB

import logging

logger = logging.getLogger()


class BaseCatalog:

    def __init__(self, table, id=None):
        self.table = table
        self.id = id

    def get_status_dict(self, db=None):
        if not db:
            db = AlchemyDB()
        db_status_list = db.find("status")
        status_dict = {}
        for db_status in db_status_list:
            status_dict[db_status['id']] = db_status
        return status_dict

    def get(self):
        if not self.id:
            return None
        db = AlchemyDB()
        result = db.find_one(self.table, id=self.id)
        status_dict = self.get_status_dict()
        logger.debug(result)
        logger.debug(status_dict)
        result["status"] = status_dict[result['status_id']]
        return result

    def get_list(self):
        db = AlchemyDB()
        result = db.find(self.table)
        status_dict = self.get_status_dict()
        logger.debug(result)
        logger.debug(status_dict)
        for r in result:
            r["status"] = status_dict[r['status_id']]
        return result

    def create(self, args):
        db = AlchemyDB()
        self.id = db.insert_row(self.table, **args)
        return self.get()

    def update(self, args):
        db = AlchemyDB()
        db.update_row_new(self.table, where={"id": self.id}, val=args)
        return self.get()


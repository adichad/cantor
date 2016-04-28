import uuid
import binascii
import logging
from sqlalchemydb import AlchemyDB
from base_catalog import BaseCatalog

logger = logging.getLogger()


class HubServiceability(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "hub_serviceability", id)

    def get_detailed_list(self, limit, offset):
        db = AlchemyDB()

        result = db.find(self.table, _limit=limit, _offset=offset)
        total_results = db.count_rows(self.table)

        status_dict = self.get_status_dict(db)
        for r in result:
            r["status"] = status_dict[r['status_id']]
        return result, total_results


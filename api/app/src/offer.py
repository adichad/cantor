import logging
from base_catalog import BaseCatalog

logger = logging.getLogger()


class Offer(BaseCatalog):

    def __init__(self, id=None):
        BaseCatalog.__init__(self, "offer", id)

    def get_offer(self):
        return self.get()

    def create_offer(self, offer_data):
        offer_args = {
            'discount_percent'      : offer_data['discount_percent'],
            'discount_cap_amount'   : offer_data['discount_cap_amount'],
            'valid_from'            : offer_data['valid_from'],
            'valid_thru'            : offer_data['valid_thru'],
            'status_id'             : offer_data['status_id']
        }
        db = AlchemyDB()
        self.id = db.insert_row(self.table, **offer_args)
        offer_subscription_args = []
        for s in offer_data['subscriptions']:
            offer_subscription_args.append({
                'offer_id'          : self.id,
                'subscription_id'   : s['subscription_id'],
                'quantity'          : s['quantity'],
                'status_id'         : offer_data['status_id']
            })
        db.insert_row_batch("offer_subscription", offer_subscription_args)
        return self.get_offer()


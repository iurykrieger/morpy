from database.db import db
import pymongo
from app.api.metadata.ItemMetadata import ItemMetadata

class ItemMetadataService(object):

    def __init__(self):
        self.item_meta = db.item_metadata

    def get_active(self):
        return self.item_meta.find_one({'active': True})

    def insert(self, item_meta_dict):
        return self.item_meta.insert(item_meta_dict)

    def disable_all(self):
        return self.item_meta.update({'active': True}, {'$set': {'active': False}})

    def get_all(self):
        return self.item_meta.find().sort([('version', pymongo.DESCENDING)])
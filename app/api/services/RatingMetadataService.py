from database.db import db
import pymongo


class RatingMetadataService(object):

    def __init__(self):
        self.rating_meta = db.rating_metadata

    def get_active(self):
        return self.rating_meta.find_one({'active': True})

    def insert(self, rating_meta_dict):
        return self.rating_meta.insert(rating_meta_dict)

    def disable_all(self):
        return self.rating_meta.update({'active': True}, {'$set': {'active': False}})
            
    def get_all(self):
        return self.rating_meta.find().sort([('version', pymongo.DESCENDING)])
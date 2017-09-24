from database.db import db
import pymongo


class UserMetadataService(object):

    def __init__(self):
        self.user_meta = db.user_metadata

    def get_active(self):
        return self.user_meta.find_one({'active': True})

    def insert(self, user_meta_dict):
        return self.user_meta.insert(user_meta_dict)

    def disable_all(self):
        return self.user_meta.update({'active': True}, {'$set': {'active': False}})
            
    def get_all(self):
        return self.user_meta.find().sort([('version', pymongo.DESCENDING)])
from database.db import db, ObjectIDConverter
from pymongo import ReturnDocument

class ItemService(object):

    def __init__(self):
        self.items = db.items

    def get_by_id(self, item_id):
        return self.items.find_one({'_id': item_id})

    def get_all(self):
        return self.items.find({}, {'similar': 0})

    def get_similar_info(self, similar_list):
        return self.items.find({'_id': {'$in' : similar_list}}, {'similar': 0})

    def insert(self, item_dict):
        return  ObjectIDConverter.to_url(self.items.insert(item_dict))

    def update_recommendations(self, item_id, recommendations):
        self.items.find_one_and_update(
            {'_id': item_id},
            {'$set': {'similar': recommendations}}
        )
from database.db import db, ObjectIDConverter
from pymongo import ReturnDocument


class RatingService(object):

    def __init__(self):
        self.ratings = db.ratings

    def get_by_id(self, rating_id):
        return self.ratings.find_one({'_id': rating_id})

    def get_all(self):
        return self.ratings.find()

    def update(self, rating_id, new_data):
        return self.ratings.find_one_and_update(
            {'_id': rating_id},
            {'$set': {
                'name': new_data['name'],
                'age': new_data['age'],
                'email': new_data['email']
            }},
            return_document=ReturnDocument.AFTER
        )

    def insert(self, rating_dict):
        return ObjectIDConverter.to_url(self.ratings.insert(rating_dict))

    def remove(self, rating_id):
        return self.ratings.remove({'_id': rating_id})

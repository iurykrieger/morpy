from database.db import db, ObjectIDConverter
from app.api.metadata.ItemMetadata import ItemMetadata
from app.api.services.ItemMetadataService import ItemMetadataService
import pymongo

class ItemService(object):

    def __init__(self):
        self.items = db.items
        self.meta = ItemMetadata(ItemMetadataService().get_active())

    def get_by_id(self, item_id):
        return self.items.find_one({'_id': item_id})

    def get_all(self):
        return self.items.find({}, {'similar': 0})

    def get_info(self, item_list):
        return self.items.find({'_id': {'$in' : item_list}}, {'similar': 0})

    def insert(self, item_dict):
        return self.items.insert(item_dict)

    def remove(self, item_id):
        return self.items.remove({'_id': item_id})

    def update_recommendations(self, item_id, recommendations):
        return self.items.find_one_and_update(
            {'_id': item_id},
            {'$set': {'similar': recommendations}}
        )

    def get_rec_data(self):
        attributes = self.meta.get_recommendable_attributes()
        coalesce_attributes = {'$project': {}}
        concat_filter = {'$project': {}}

        for attr in attributes:
            coalesce_attributes['$project'][attr] = {
                '$ifNull': ['${name}'.format(name=attr), '']}

        concat_filter['$project']['concated_attrs'] = {
            '$concat': ['${name}'.format(name=attr) for attr in attributes]}

        return self.items.aggregate([coalesce_attributes, concat_filter])
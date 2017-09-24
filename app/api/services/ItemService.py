from database.db import db, ObjectIDConverter
from app.api.metadata.ItemMetadata import ItemMetadata
from app.api.services.ItemMetadataService import ItemMetadataService

class ItemService(object):

    def __init__(self):
        self.items = db.items
        self.meta = ItemMetadata(ItemMetadataService().get_active())

    def get_by_id(self, item_id):
        return self.items.find_one({'_id': item_id})

    def get_all(self):
        return self.items.find({}, {'similar': 0})

    def get_similar_info(self, similar_list):
        return self.items.find({'_id': {'$in' : similar_list}}, {'similar': 0})

    def insert(self, item_dict):
        return  ObjectIDConverter.to_url(self.items.insert(item_dict))

    def update_recommendations(self, item_id, recommendations):
        return self.items.find_one_and_update(
            {'_id': item_id},
            {'$set': {'similar': recommendations}}
        )

    def _get_recommendable_attributes(self):
        return [attribute['name'] for attribute in self.meta.attributes
                if attribute['recommendable'] and attribute['type'] == 'string']

    def get_rec_data(self):
        attributes = self._get_recommendable_attributes()
        coalesce_attributes = {'$project': {}}
        concat_filter = {'$project': {}}

        for attr in attributes:
            coalesce_attributes['$project'][attr] = {
                '$ifNull': ['${name}'.format(name=attr), '']}

        concat_filter['$project']['concated_attrs'] = {
            '$concat': ['${name}'.format(name=attr) for attr in attributes]}

        return self.items.aggregate([coalesce_attributes, concat_filter])
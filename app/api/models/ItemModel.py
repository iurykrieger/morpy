from app.api.metadata.ItemMetadata import ItemMetadata, TYPE_MAPPING
from database.db import db, ObjectIDConverter


class ItemModel(object):
    def __init__(self, item):
        self.meta = ItemMetadata(db.item_metadata.find_one({'active': True}))
        self.item = item

    def _get_existent_attributes(self):
        return [attr for attr in self.meta.attributes if attr['name'] in self.item]

    def _validate(self):
        for attr in self.meta.attributes:
            if attr['name'] not in self.item:
                return False
            elif TYPE_MAPPING[type(self.item[attr['name']]).__name__] != attr['type']:
                return False
        return True

    def to_json(self):
        json = {
            '_id': ObjectIDConverter.to_url(self.item['_id'])
        }
        for attr in self._get_existent_attributes():
            json[attr['name']] = self.item[attr['name']]
        return json

    def to_rec_json(self, similarity=0):
        json = self.to_json()
        json['similarity'] = similarity
        return json

from app.api.metadata.ItemMetadata import ItemMetadata, TYPE_MAPPING
from app.api.services.ItemMetadataService import ItemMetadataService
from database.db import ObjectIDConverter

class ItemModel(object):
    def __init__(self, item):
        self.meta_service = ItemMetadataService()
        self.meta = ItemMetadata(self.meta_service.get_active())
        self.item = item

    def _get_existent_attributes(self):
        return [attr for attr in self.meta.attributes 
            if (attr['name'] in self.item) and  ('hide' not in attr)]

    def validate(self):
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

from app.api.metadata.RatingMetadata import RatingMetadata
from app.api.services.RatingMetadataService import RatingMetadataService
from database.db import ObjectIDConverter
from app.common.exceptions import StatusCodeException
from app.common.mapping import get_synonymous


class RatingModel(object):
    def __init__(self, rating):
        self.rating_service = RatingMetadataService()
        self.meta = RatingMetadata(self.rating_service.get_active())
        self.rating = rating

    def _get_existent_attributes(self):
        return [
            attr for attr in self.meta.attributes
            if (attr['name'] in self.rating) and ('hide' not in attr)
        ]

    def validate(self):
        for attr in self.meta.attributes:
            if attr['name'] not in self.rating:
                if 'nullable' not in attr or not attr['nullable']:
                        raise StatusCodeException('Missing %s attribute' % attr['name'], 400)
            elif get_synonymous(type(self.rating[attr['name']]).__name__) != attr['type']:
                raise StatusCodeException('%s attribute has wrong type' % attr['name'], 400)
        return True

    def to_database(self):
        rating = {}
        for attr in self.meta.attributes:
            if attr['name'] in self.rating:
                rating[attr['name']] = self.rating[attr['name']]
        return rating

    def set_id(self, rating_id):
        self.rating['_id'] = rating_id

    def to_json(self):
        json = {'_id': ObjectIDConverter.to_url(self.rating['_id'])}
        for attr in self._get_existent_attributes():
            json[attr['name']] = self.rating[attr['name']]
        return json

    def to_rec_json(self, similarity=0):
        json = self.to_json()
        json['similarity'] = similarity
        return json

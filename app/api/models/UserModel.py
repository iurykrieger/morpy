from app.api.metadata.UserMetadata import UserMetadata
from database.db import ObjectIDConverter
from app.api.services.UserMetadataService import UserMetadataService
from app.common.exceptions import StatusCodeException
from app.common.mapping import get_synonymous

class UserModel(object):
    def __init__(self, user):
        self.meta_service = UserMetadataService()
        self.meta = UserMetadata(self.meta_service.get_active())
        self.user = user

    def _get_existent_attributes(self):
        return [attr for attr in self.meta.attributes
            if (attr['name'] in self.user) and  ('hide' not in attr)]

    def validate(self):
        for attr in self.meta.attributes:
            if attr['name'] not in self.user:
                if 'nullable' not in attr or not attr['nullable']:
                        raise StatusCodeException('Missing %s attribute' % attr['name'], 400)
            elif get_synonymous(type(self.user[attr['name']]).__name__) != attr['type']:
                raise StatusCodeException('%s attribute has wrong type' % attr['name'], 400)
        return True

    def set_id(self, user_id):
        self.user['_id'] = user_id

    def to_database(self):
        item = {}
        for attr in self.meta.attributes:
            if attr['name'] in self.user:
                item[attr['name']] = self.user[attr['name']]
        return item

    def to_json(self):
        json = {
            '_id': ObjectIDConverter.to_url(self.user['_id'])
        }
        for attr in self._get_existent_attributes():
            json[attr['name']] = self.user[attr['name']]
        return json

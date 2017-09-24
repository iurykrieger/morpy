from app.api.metadata.UserMetadata import UserMetadata, TYPE_MAPPING
from database.db import db, ObjectIDConverter


class UserModel(object):
    def __init__(self, user):
        self.meta = UserMetadata(db.user_metadata.find_one({'active': True}))
        self.user = user

    def _get_existent_attributes(self):
        return [attr for attr in self.meta.attributes 
            if (attr['name'] in self.user) and  ('hide' not in attr)]

    def _validate(self):
        for attr in self.meta.attributes:
            if attr['name'] not in self.user:
                return False
            elif TYPE_MAPPING[type(self.user[attr['name']]).__name__] != attr['type']:
                return False
        return True

    def to_json(self):
        json = {
            '_id': ObjectIDConverter.to_url(self.user['_id'])
        }
        for attr in self._get_existent_attributes():
            json[attr['name']] = self.user[attr['name']]
        return json

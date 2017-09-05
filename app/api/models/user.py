from app.common.exceptions import StatusCodeException
from database.db import ObjectIDConverter


class User(object):

    def __init__(self, user):
        try:
            if '_id' in user:
                self._id = user['_id']
            self.email = user['email']
            self.password = user['password']
            self.name = user['name']
            self.age = user['age']
        except:
            raise StatusCodeException('Missing fields', 400)

    def to_json(self):
        return {
            '_id': ObjectIDConverter.to_url(self._id),
            'email': self.email,
            'name': self.name,
            'age': self.age
        }

    def to_database(self):
        return {
            'email': self.email,
            'name': self.name,
            'age': self.age,
            'password': self.password
        }

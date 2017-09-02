from app.common.exceptions import StatusCodeException
from database.db import db, ObjectIDConverter


class User(object):

    def __init__(self, json):
        self.users = db.users
        try:
            self._id = None
            self.email = json['email']
            self.password = json['password']
            self.name = json['name']
            self.age = json['age']
        except:
            raise StatusCodeException('Missing fields', 400)

    def exists(self):
        return self.users.find_one({
            'email': self.email,
            'password': self.password
        })

    def save(self):
        if not self.exists():
            self._id = self.users.insert(self.to_database())
            return self.to_json()
        else:
            raise StatusCodeException('Conflict', 409)

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

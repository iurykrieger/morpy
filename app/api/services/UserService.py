from database.db import db, ObjectIDConverter
from pymongo import ReturnDocument


class UserService(object):

    def __init__(self):
        self.users = db.users

    def get_by_token(self, token):
        return self.users.find_one({'auth.token': token})

    def get_by_id(self, user_id):
        return self.users.find_one({'_id': user_id})

    def get_all(self):
        return self.users.find()

    def expire_token(self, user_id, token):
        return self.users.find_one_and_update(
            {'_id': user_id},
            {'$set': {
                'auth': {'token': token, 'valid': False}
            }}
        )

    def update(self, user_id, new_data):
        return self.users.find_one_and_update(
            {'_id': user_id},
            {'$set': {
                'name': new_data['name'],
                'age': new_data['age'],
                'email': new_data['email']
            }},
            return_document=ReturnDocument.AFTER
        )

    def insert(self, user_dict):
        return self.users.insert(user_dict)

    def remove(self, user_id):
        return self.users.remove({'_id': user_id})

    def remove_token(self, user_id):
        return self.users.find_one_and_update(
            {'_id': user_id},
            {'$set': {
                'auth': {}
            }}
        )

    def exists(self, email):
        return self.users.find_one({'email': email})

    def verify(self, email, password):
        user = self.users.find_one({'email': email, 'password': password})
        if user:
            return user['_id']
        return False

    def update_token(self, user_id, new_token):
        return self.users.find_one_and_update(
            {'_id': user_id},
            {'$set': {
                'auth': {'token': new_token, 'valid': True}
            }}
        )

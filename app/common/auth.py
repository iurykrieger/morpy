from functools import wraps
from flask import request, abort
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from database.db import mongo_client

class Auth(object):

    def __init__(self, secret_key):
        self.users = mongo_client.db.users
        self.secret_key = secret_key

    def generate_token(self, email, password, expiration=1296000):  # 15 days token
        user = self.users.find_one({'email': email, 'password': password})
        if user:
            serializer = Serializer(self.secret_key, expires_in=expiration)
            token = serializer.dumps({'email': email, 'password': password})
            self.users.find_one_and_update(
                {'_id': user['_id']},
                {'$set': {
                    'auth': {'token': token, 'valid': True}
                }});
            return token
        else:
            return None

    def authenticate(self, token):
        user = self.users.find_one({'token': token})
        if user:
            try:
                serializer = Serializer(self.secret_key)
                serializer.loads(user['auth']['token'])
                return True
            except SignatureExpired:
                self.users.find_one_and_update(
                    {'_id': user['_id']},
                    {'$set': {
                        'auth': {'token': token, 'valid': False}
                    }});
                return False  # valid token, but expired
            except BadSignature:
                self.users.find_one_and_update(
                    {'_id': user['_id']},
                    {'$set': {
                        'auth': {}
                    }});
                return False  # invalid token
        else:
            return False

    def middleware_auth_token(self, function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('token', None)
            if not self.authenticate(token):
                abort(403)
            return function(*args, **kwargs)
        return decorated_function

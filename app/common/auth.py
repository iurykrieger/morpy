from pymongo import MongoClient
from flask import request, abort
from functools import wraps
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


class Auth(object):

    def __init__(self, secret_key):
        self.auth = MongoClient().db.auth
        self.secret_key = secret_key

    def generate_token(self, user, expiration=1296000):  # 15 days token
        serializer = Serializer(self.secret_key, expires_in=expiration)
        token = serializer.dumps({'email': user['email']})
        self.auth.insert({'token': token, 'expiration': expiration})
        return token

    def authenticate(self, token):
        token = self.auth.find_one({'token': token})
        if token:
            try:
                serializer = Serializer(self.secret_key)
                email = serializer.loads(token['token'])
                if email:
                    return True
            except SignatureExpired:
                return False  # valid token, but expired
            except BadSignature:
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

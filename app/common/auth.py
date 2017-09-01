import mongo
from functools import wraps
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


class Auth(object):

    def __init__(self, secret_key):
        self.auth_collection = mongo.get_db().db.auth
        self.secret_key = secret_key

    def generate_token(self, user, expiration=1296000):  # 15 days token
        serializer = Serializer(self.secret_key, expires_in=expiration)
        token = serializer.dumps({'_id': user['_id']})
        self.auth_collection.insert({'token': token, 'expiration': expiration})
        print token
        return token

    @staticmethod
    def authenticate(self, token):
        token = self.auth_collection.find_one({'token': token})
        if token:
            try:
                user_id = serializer.loads(token['token'])
            except SignatureExpired:
                return False  # valid token, but expired
            except BadSignature:
                return False  # invalid token
        else:
            return False



def middleware_auth_token(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('token', None)
        if not Auth.authenticate(token):
            abort(403)
        return function(*args, **kwargs)
    return decorated_function

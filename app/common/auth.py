from functools import wraps
from flask import request
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, 
    BadSignature, SignatureExpired)
from settings import SECRET_KEY
from app.api.services.UserService import UserService
from app.common.exceptions import StatusCodeException


class Auth(object):

    def __init__(self, secret_key):
        self.service = UserService()
        self.secret_key = secret_key

    def generate_token(self, email, password, expiration=1296000):  # 15 days token
        user_id = self.service.verify(email, password)
        if user_id:
            serializer = Serializer(self.secret_key, expires_in=expiration)
            token = serializer.dumps({'email': email, 'password': password})
            self.service.update_token(user_id, token)
            return token
        else:
            raise StatusCodeException('User not found', 404)

    def authenticate(self, token):
        user = self.service.get_by_token(token)
        if user:
            try:
                serializer = Serializer(self.secret_key)
                serializer.loads(user['auth']['token'])
                return True
            except SignatureExpired:
                self.service.expire_token(user['_id'], token)
                return False  # valid token, but expired
            except BadSignature:
                self.service.remove_token(user['_id'])
                return False  # invalid token
        else:
            return False

    def middleware_auth_token(self, function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            try:
                # XXX - Reenable token when finish
                #token = request.headers.get('token', None)
                #if not token or not self.authenticate(token):
                #    raise StatusCodeException('Not authorized', 403)
                return function(*args, **kwargs)
            except StatusCodeException as ex:
                return ex.to_response()
            except Exception as ex:
                return StatusCodeException(ex.message, 500).to_response()

        return decorated_function

auth = Auth(SECRET_KEY)

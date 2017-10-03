from flask_restful import Resource
from flask import request, make_response
from app.common.exceptions import StatusCodeException
from app.common.auth import auth


class Token(Resource):

    ENDPOINT = '/auth/token'

    def post(self):
        try:
            email = request.data.get('email', None)
            password = request.data.get('password', None)
            if email and password:
                token = auth.generate_token(email, password)
                return make_response({'token': token})
            else:
                raise StatusCodeException('Invalid parameters', 400)
        except StatusCodeException as ex:
            return ex.to_response()
        except Exception as ex:
            return StatusCodeException(ex.message, 500).to_response()

from flask import make_response


class StatusCodeException(Exception):

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_response(self):
        response = make_response({
            'message': self.message,
            'status': self.status_code
        })
        response.status_code = self.status_code
        return response

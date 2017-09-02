from flask import jsonify


class StatusCodeException(Exception):

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_json(self):
        return {"status": self.status_code, "message": self.message}

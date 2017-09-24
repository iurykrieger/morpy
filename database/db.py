from settings import MONGO_DBNAME, MONGO_USERNAME, MONGO_PASSWORD, MONGO_PORT, MONGO_HOST
from pymongo import MongoClient
from werkzeug.routing import BaseConverter, ValidationError
from itsdangerous import base64_encode, base64_decode
from bson.objectid import ObjectId
from bson.errors import InvalidId

MONGO_URI = 'mongodb://%s:%s@%s:%s/%s' % (MONGO_USERNAME, MONGO_PASSWORD,
                                          MONGO_HOST, MONGO_PORT, MONGO_DBNAME)


class ObjectIDConverter(BaseConverter):
    @staticmethod
    def to_python(value):
        try:
            return ObjectId(base64_decode(value))
        except (InvalidId, ValueError, TypeError):
            raise ValidationError()

    @staticmethod
    def to_url(value):
        return base64_encode(value.binary)


def get_db():
    return MongoClient(MONGO_URI, connect=False, maxPoolSize=200)[MONGO_DBNAME]


db = get_db()

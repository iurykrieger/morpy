from app.common.exceptions import StatusCodeException
from datetime import datetime


class ItemMetadata(object):
    def __init__(self, metadata):
        try:
            self._id = metadata['_id'] if '_id' in metadata else None
            self.type = metadata['type']
            self.attributes = metadata['attributes']
        except StatusCodeException as ex:
            raise ex
        except Exception as ex:
            raise StatusCodeException('Missing fields', 400)

    def to_database(self):
        return {
            'type': self.type,
            'attributes': self.attributes,
            'active': True,
            'created_at': datetime.now()
        }

    def to_json(self):
        return {
            'type': self.type,
            'attributes': self.attributes,
            'active': True
        }

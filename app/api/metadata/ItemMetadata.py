from app.common.exceptions import StatusCodeException
from datetime import datetime
<<<<<<< HEAD
=======

TYPE_MAPPING = {'unicode': 'string', 'string': 'string'}
>>>>>>> af8dd5f8dd191a6c8ad09a3f2dcc8dbe8453512e


class ItemMetadata(object):
    def __init__(self, metadata, version=1, active=False):
        try:
<<<<<<< HEAD
            self._id = metadata['_id'] if '_id' in metadata else None
            self.type = metadata['type']
            self.attributes = metadata['attributes']
=======
            self.meta = metadata
            self.type = self.meta['type']
            self.attributes = self.meta['attributes']
            self.active = self.meta['active'] if 'active' in self.meta else active
            self.created_at = self.meta['created_at'] if 'created_at' in self.meta else datetime.now()
            self.version = self.meta['version'] if 'version' in self.meta else version

            if self.type != 'item':
                raise StatusCodeException('Invalid type', 400)

            if self.attributes:
                for attribute in self.attributes:
                    if 'name' not in attribute:
                        raise StatusCodeException(
                            'Missing metadata attribute name.', 400)
                    elif 'type' not in attribute:
                        raise StatusCodeException(
                            'Missing "%s" type' % attribute['name'], 400)
            else:
                raise StatusCodeException('Empty metadata attributes', 400)
>>>>>>> af8dd5f8dd191a6c8ad09a3f2dcc8dbe8453512e
        except StatusCodeException as ex:
            raise ex
        except Exception as ex:
            raise StatusCodeException('Missing metadata fields', 400)

    def to_database(self):
        return {
            'type': self.type,
            'attributes': self.attributes,
            'active': self.active,
            'created_at': self.created_at,
            'version': self.version
        }

    def to_json(self):
        return {
            'type': self.type,
            'attributes': self.attributes,
            'active': self.active,
            'created_at': self.created_at,
            'version': self.version
        }

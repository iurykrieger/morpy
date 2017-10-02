from app.common.exceptions import StatusCodeException
from datetime import datetime

TYPE_MAPPING = {'unicode': 'string', 'string': 'string', 'int' : 'int'}


class ItemMetadata(object):
    def __init__(self, metadata, version=1, active=False):
        if not metadata:
            raise StatusCodeException('Item metadata not found', 404)

        self.meta = metadata
        self.type = self.meta['type']
        self.attributes = self.meta['attributes']
        self.active = self.meta['active'] if 'active' in self.meta else active
        self.created_at = self.meta[
            'created_at'] if 'created_at' in self.meta else datetime.now()
        self.version = self.meta[
            'version'] if 'version' in self.meta else version

        if self.type != 'item':
            raise StatusCodeException('Invalid type', 400)

        if self.attributes:
            for attribute in self.attributes:
                if 'name' not in attribute:
                    raise StatusCodeException(
                        'Missing name attribute at item metadata', 400)
                elif 'type' not in attribute:
                    raise StatusCodeException(
                        'Missing type for "%s" at item metadata' %
                        attribute['name'], 400)
        else:
            raise StatusCodeException('Missing attributes for item metadata',
                                      400)

    def get_nullable_attributes(self):
        return [
            attribute for attribute in self.attributes if 'nullable' not in attribute or not attribute['nullable']
        ]

    def get_recommendable_attributes(self):
        return [
            attribute['name'] for attribute in self.attributes
            if attribute['recommendable'] and attribute['type'] == 'string'
        ]

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

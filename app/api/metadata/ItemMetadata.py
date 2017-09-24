from app.common.exceptions import StatusCodeException
from datetime import datetime

TYPE_MAPPING = {'unicode': 'string', 'string': 'string'}


class ItemMetadata(object):
    def __init__(self, metadata, version=1, active=False):
        try:
            self.meta = metadata
            self.type = self.meta['type']
            self.attributes = self.meta['attributes']
            self.active = self.meta['active'] if 'active' in self.meta else active
            self.created_at = self.meta['created_at'] if 'created_at' in self.meta else datetime.now()
            self.version = self.meta['version'] if 'version' in self.meta else version

            if self.type != 'item':
                raise StatusCodeException('Invalid type', 400)

            if len(self.attributes) > 0:
                for attribute in self.attributes:
                    if 'name' not in attribute:
                        raise StatusCodeException('Missing metadata attribute name.', 400)
                    elif 'type' not in attribute:
                        raise StatusCodeException(
                            'Missing "%s" type' % attribute['name'], 400)
            else:
                raise StatusCodeException('Empty metadata attributes', 400)
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


"""
{
    "type" : "item",
    "attributes": [
        {
            "name": "title",
            "wheight" : 10,
            "unique": true,
            "type" : "string",
            "max_length": 120,
            "recommendable": true
        },
        {
            "name": "description",
            "wheight" : 10,
            "unique": false,
            "type": "string",
            "recommendable": true
        },
        //...
    ]
}
"""

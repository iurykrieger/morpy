from app.common.exceptions import StatusCodeException
from datetime import datetime
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

TYPE_MAPPING = {'unicode': 'string', 'string': 'string'}


class UserMetadata(object):
    def __init__(self, metadata):
        try:
            self.type = metadata['type']
            self.attributes = metadata['attributes']

            if self.type != 'item':
                raise StatusCodeException('Invalid type', 400)

            if len(self.attributes) > 0:
                for attribute in self.attributes:
                    if 'name' not in attribute:
                        raise StatusCodeException('Missing attribute name',
                                                  400)
                    elif 'type' not in attribute:
                        raise StatusCodeException(
                            'Missing "%s" type' % attribute['name'], 400)
            else:
                raise StatusCodeException('Empty attributes', 400)
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

from app.common.exceptions import StatusCodeException
from Validator import Validator
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


class ItemValidator(Validator):
    def __init__(self, metadata, item):
        self.metadata = metadata
        self.item = item
        self.TYPE_MAPPING = {'unicode': 'string', 'string': 'string'}

    def validate(self):
        for attr in self.metadata.attributes:
            if attr['name'] not in self.item:
                return False
            elif self.TYPE_MAPPING[type(self.item[attr['name']])
                                   .__name__] != attr['type']:
                return False
        return True

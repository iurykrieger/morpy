from app.common.exceptions import StatusCodeException


class ItemMetadataValidator(Validator):
    def __init__(self, metadata):
        self.metadata = metadata

    def validate(self):
        if self.metadata.type != 'item':
            raise StatusCodeException('Invalid type', 400)

        if len(self.metadata.attributes) > 0:
            for attribute in self.metadata.attributes:
                if 'name' not in attribute:
                    raise StatusCodeException('Missing attribute name', 400)
                elif 'type' not in attribute:
                    raise StatusCodeException(
                        'Missing "%s" type' % attribute['name'], 400)
        else:
            raise StatusCodeException('Empty attributes', 400)

        return True

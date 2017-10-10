from app.common.exceptions import StatusCodeException
from datetime import datetime


class RatingMetadata(object):
    """
    This class creates and validates a given rating metadata dict to store it
    as internal attributes.

    Args:
        - metadata (dict): An rating metadata dict representation.
        - version (int): The current version of rating metadata representation.
        - active (boolean): A boolean to tell if the given dict is the current active in database.
    """

    def __init__(self, metadata, version=1, active=False):
        if not metadata:
            raise StatusCodeException('Rating metadata not found', 404)

        self.meta = metadata
        self.type = self.meta['type']
        self.attributes = self.meta['attributes']
        self.active = self.meta['active'] if 'active' in self.meta else active
        self.created_at = self.meta['created_at'] if 'created_at' in self.meta else datetime.now()
        self.version = self.meta['version'] if 'version' in self.meta else version

        if self.type != 'rating':
            raise StatusCodeException('Invalid type', 400)

        if self.attributes:
            for attribute in self.attributes:
                if 'name' not in attribute:
                    raise StatusCodeException('Missing name attribute at item metadata', 400)
                elif 'type' not in attribute:
                    raise StatusCodeException('Missing type for "%s" at item metadata' %
                        attribute['name'], 400)
        else:
            raise StatusCodeException('Missing attributes for item metadata', 400)

    def get_required_attributes(self):
        """
        Return all item metadata required attributes.

        It iterates over the metadata attributes finding all required ones. 

        Returns:
            An array with all rating required attributes

        """
        return [
            attribute for attribute in self.attributes if 'nullable' not in attribute or not attribute['nullable']
        ]

    def get_recommendable_attributes(self):
        """
        Return all rating metadata recommendable attributes.

        It iterates over the metadata attributes finding all recommendable ones.

        Returns:
            An array with all rating recommendable attributes

        """
        return [
            attribute['name'] for attribute in self.attributes
            if 'recommendable' in attribute and attribute['recommendable'] and attribute['type'] == 'string'
        ]

    def to_database(self):
        """
        Builds a BSON representation of the metadata to be stored in mongoDB database.

        It uses Metadata class attributes to buil a BSON object.

        Returns:
            A BSON dict to be stored.
        """
        return {
            'type': self.type,
            'attributes': self.attributes,
            'active': self.active,
            'created_at': self.created_at,
            'version': self.version
        }

    def to_json(self):
        """
        Builds a JSON representation of the metadata to be returned as API output to user.

        It uses Metadata class attributes to build a JSON object.

        Returns:
            A JSON dict to be returned as API output.
        """
        return {
            'type': self.type,
            'attributes': self.attributes,
            'active': self.active,
            'created_at': self.created_at,
            'version': self.version
        }

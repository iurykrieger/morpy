from app.api.metadata.ItemMetadata import ItemMetadata
from app.api.services.ItemMetadataService import ItemMetadataService
from database.db import ObjectIDConverter
from app.common.exceptions import StatusCodeException
from app.common.mapping import get_synonymous


class ItemModel(object):
    """
    This class creates, manage and validates a given item dict to store it
    in database and ouput it to all requests.

    Args:
        - item (dict): An item dict representation.
    """

    def __init__(self, item):
        self.meta_service = ItemMetadataService()
        self.meta = ItemMetadata(self.meta_service.get_active())
        self.item = item

    def _get_existent_attributes(self):
        return [
            attr for attr in self.meta.attributes
            if (attr['name'] in self.item) and ('hide' not in attr)
        ]

    def validate(self):
        """
        Validates existent item attributes based on current
        item metadata.

        It uses item metadata definitions to validate item
        dynamic attributes and values.

        Returns:
            ``True`` if all item attributes match with metadata. Otherwise,
            throw an Exception to eatch type of validation.
        """
        for attr in self.meta.attributes:
            if attr['name'] not in self.item:
                if 'nullable' not in attr or not attr['nullable']:
                        raise StatusCodeException('Missing %s attribute' % attr['name'], 400)
            elif get_synonymous(type(self.item[attr['name']]).__name__) != attr['type']:
                raise StatusCodeException('%s attribute has wrong type' % attr['name'], 400)
        return True

    def to_database(self):
        """
        Builds a BSON representation of the item to be stored in database.

        It uses Item class existent attributes to build a BSON object.

        Returns:
            A BSON dict to be stored.
        """
        item = {}
        for attr in self.meta.attributes:
            if attr['name'] in self.item:
                item[attr['name']] = self.item[attr['name']]
        return item

    def set_id(self, item_id):
        """
        Sets user_id to Item class after it have been generated in database.

        Args:
            - item_id (objectId): The correspondent item_id in database.

        Returns:
            None
        """
        self.item['_id'] = item_id

    def to_json(self):
        """
        Builds a JSON representation of the item to be returned as API output to user.

        It uses Item class existent attributes to build a JSON object.

        Returns:
            A JSON dict to be returned as API output.
        """
        json = {'_id': ObjectIDConverter.to_url(self.item['_id'])}
        for attr in self._get_existent_attributes():
            json[attr['name']] = self.item[attr['name']]
        return json

    def to_rec_json(self, similarity=0):
        """
        Builds a JSON representation of the item to be returned as API
        recommendation utput.

        It uses Item class existent attributes to build a JSON object
        that contains item attributes and similarity level.

        Returns:
            A JSON dict to be returned as API output.
        """
        json = self.to_json()
        json['similarity'] = similarity
        return json

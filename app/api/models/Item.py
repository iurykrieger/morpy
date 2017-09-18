class Item(object):
    def __init__(self):
        pass

    def validate(self, metadata):
        for attr in metadata.attributes:
            if attr['name'] not in item:
                return False
            elif TYPE_MAPPING[type(item[attr['name']])
                              .__name__] != attr['type']:
                return False
        return True
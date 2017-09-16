from database.db import ObjectIDConverter

def to_json(bson_item):
    bson_item['_id'] = ObjectIDConverter.to_url(bson_item['_id'])
    return bson_item
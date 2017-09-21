from database.db import ObjectIDConverter

def to_json(bson_item):
    return {
        '_id' : ObjectIDConverter.to_url(bson_item['_id']),
        'title': bson_item['title'],
        'genres': bson_item['genres'],
    }
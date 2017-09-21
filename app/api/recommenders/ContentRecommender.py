from Recommender import Recommender
from database.db import db, ObjectIDConverter
from app.api.models.ItemModel import ItemModel
from app.common.adapter import to_json
from app.common.exceptions import StatusCodeException


class ContentRecommender(Recommender):
    def __init__(self):
        self.items = db.items

    def recommend(self, item_id, number_of_recommendations=10):
        """
        Couldn't be simpler! Just retrieves the similar items and their 'score' from redis.

        :param item_id: int
        :param number_of_recommendations: number of similar items to return
        :return: A list of lists like: [["19", 0.2203], ["494", 0.1693], ...]. The first item in each sub-list is
        the item ID and the second is the similarity score. Sorted by similarity score, descending.
        """
        item = self.items.find_one({'_id': item_id})
        if item:
            if 'similar' in item:
                similar_items = item['similar'][:number_of_recommendations]
                similar_ids = [it['_id'] for it in item['similar'][:number_of_recommendations]]
                recommendations = self.items.find({'_id': {'$in' : similar_ids}}, {'similar': 0})
                json_recs = []
                for rec in recommendations:
                    for similar_item in similar_items:
                        if similar_item['_id'] == rec['_id']:
                            json_recs.append(ItemModel(rec).to_rec_json(similar_item['similarity']))
                return json_recs
            return {}
        else:
            raise StatusCodeException('No item found', 404)


content_recommender = ContentRecommender()
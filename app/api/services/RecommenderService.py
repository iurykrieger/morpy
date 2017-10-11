from app.api.models.ItemModel import ItemModel
from app.common.exceptions import StatusCodeException
from app.api.services.ItemService import ItemService
from app.api.services.RatingService import RatingService
import operator

class RecommenderService(object):
    def __init__(self):
        self.item_service = ItemService()
        self.ratings = RatingService()

    def recommend(self, item_id, start=0, end=10):
        """
        Couldn't be simpler! Just retrieves the similar items and their 'score' from redis.

        :param item_id: int
        :param number_of_recommendations: number of similar items to return
        :return: A list of lists like: [["19", 0.2203], ["494", 0.1693], ...]. The first item in each sub-list is
        the item ID and the second is the similarity score. Sorted by similarity score, descending.
        """
        item = self.item_service.get_by_id(item_id)
        if item:
            if 'similar' in item:
                similar_items = item['similar'][start:end]
                similar_ids = [it['_id'] for it in item['similar'][start:end]]
                recommendations = self.item_service.get_info(similar_ids)
                json_recs = []
                for rec in recommendations:
                    for similar_item in similar_items:
                        if similar_item['_id'] == rec['_id']:
                            json_recs.append(ItemModel(rec).to_rec_json(similar_item['similarity']))
                json_recs = sorted(json_recs, cmp=lambda x,y: cmp(x['similarity'], y['similarity']), reverse=True) #Resort by similarity level
                return json_recs
            return {}
        else:
            raise StatusCodeException('Item not found', 404)

    def get_shared_preferences(self, user_A, user_B):
        """
        Returns the intersection of ratings for two users
        """
        ratings = self.ratings.get_all()
        if user_A not in ratings:
            raise KeyError("Couldn't find user '%s' in data" % user_A)
        if user_B not in ratings:
            raise KeyError("Couldn't find user '%s' in data" % user_B)

        moviesA = set(ratings[user_A].keys())
        moviesB = set(ratings[user_B].keys())
        shared = moviesA & moviesB # Intersection operator

        # Create a reviews dictionary to return
        shared_prefs = {}
        for item_id in shared:
            shared_prefs[item_id] = (
                ratings[user_A][item_id]['rating'],
                ratings[user_B][item_id]['rating'],
            )
        return shared_prefs

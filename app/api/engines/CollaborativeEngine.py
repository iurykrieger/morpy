# -*- coding: utf-8 -*-
import pandas as pd
import time
import metrics
from app.common.logging import info
from app.api.services.ItemService import ItemService
from app.api.services.RatingService import RatingService
from app.api.services.UserService import UserService
from app.api.services.RecommenderService import RecommenderService


class CollaborativeEngine(object):

    def __init__(self):
        start = time.time()
        self.item_service = ItemService()
        self.user_service = UserService()
        self.rating_service = RatingService()
        self.recommender_service = Recommender_service()

        self.items = pd.DataFrame(list(self.item_service.get_all()))
        self.users = pd.DataFrame(list(self.user_service.get_all()))
        self.ratings = pd.DataFrame(list(self.rating_service.get_all()))
        self.ds = Dataset.load_builtin(self.ratings)
        info("Training data ingested in %s seconds." % (time.time() - start))

    def train(self):
        start = time.time()
        self.calculatePearsonSimilarity(self.ratings, 1, 2)
        #evaluate(algo, ds, measures=['RMSE', 'MAE'])
        info("Engine trained in %s seconds." % (time.time() - start))

    def similar_items(self, item, metric='euclidean', n=50):
        # Metric jump table
        metrics = {
            'euclidean': metrics.euclidean_distance,
            'pearson':   metrics.pearson_correlation,
        }

        distance = metrics.get(metric, None)
        ratings = pd.DataFrame(list(self.rating_service.get_all()))

        # Handle problems that might occur
        if item not in ratings['movie_id']:
            raise KeyError("Unknown item, '%s'." % item)
        if not distance or not callable(distance):
            raise KeyError("Unknown or unprogrammed distance metric '%s'." % metric)

        similar_items = {}
        for similar_item in ratings['movie_id']:
            if similar_item == item:
                continue

            similar_items[similar_item] = distance(self.recommender_service.get_shared_preferences(similar_item['user_id'], item['user_id']))

        return heapq.nlargest(n, items.items(), key=itemgetter(1))
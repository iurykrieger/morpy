# -*- coding: utf-8 -*-
import pandas as pd
import time
from app.common.logging import info
from app.api.services.ItemService import ItemService
from app.api.services.RatingService import RatingService
from app.api.services.UserService import UserService


class CollaborativeEngine(object):

    def __init__(self):
        start = time.time()
        self.item_service = ItemService()
        self.user_service = UserService()
        self.rating_service = RatingService()
        self.items = pd.DataFrame(list(self.item_service.get_all()))
        self.users = pd.DataFrame(list(self.user_service.get_all()))
        self.ratings = pd.DataFrame(list(self.rating_service.get_all()))
        info("Training data ingested in %s seconds." % (time.time() - start))

    def train(self):
        start = time.time()
        print self.ratings
        print self.items
        print self.ratings
        info("Engine trained in %s seconds." % (time.time() - start))


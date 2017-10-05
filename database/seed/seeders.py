from database.db import db
import pandas as pd
import json


class MovieLens1MSeeder(object):

    def __init__(self):
        self.items = db.items
        self.users = db.users
        self.ratings = db.ratings

    def _seed_items(self):
        attrs = ['id', 'title', 'genres']
        csv_items = pd.read_csv('storage/ml-1m/movies.dat', sep=':', names=attrs, encoding='latin1')
        self.items.insert_many(json.loads(csv_items.to_json(orient='records')))

    def _seed_users(self):
        attrs = ['id','gender','age','occupation','zipcode']
        csv_users = pd.read_csv('storage/ml-1m/users.dat', sep=':', names=attrs, encoding='latin1')
        self.users.insert_many(json.loads(csv_users.to_json(orient='records')))

    def _seed_ratings(self):
        attrs = ['user_id','movie_id','rating','timestamp']
        csv_ratins = pd.read_csv('storage/ml-1m/ratings.dat', sep=':', names=attrs, encoding='latin1')
        self.ratings.insert_many(json.loads(csv_ratins.to_json(orient='records')))

    def seed(self):
        try:
            self._seed_items()
            self._seed_users()
            self._seed_ratings()
        except Exception as ex:
            print ex


class MovieLens2MSeeder(object):

    def __init__(self):
        self.items = db.items
        self.users = db.users
        self.ratings = db.ratings

    def seed_items(self):
        csv_items = pd.read_csv('storage/ml-20m/movies.csv', sep=',', encoding='latin1')
        self.items.insert_many(json.loads(csv_items.to_json(orient='records')))
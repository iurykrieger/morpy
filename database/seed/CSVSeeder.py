from database.db import db
import pandas as pd
import json


class MovieLensItemSeeder(object):

    def __init__(self):
        self.items = db.items
        self.users = db.users
        self.ratings = db.ratings

    def seed_items(self):
        attrs = [
            'id',
            'title',
            'genres'
        ]
        csv_items = pd.read_csv('storage/ml-1m/movies.dat', sep=':', names=attrs, encoding='latin1')
        self.items.insert_many(json.loads(csv_items.to_json(orient='records')))

    def seed_users(self):
        pass

    def seed_ratings(self):
        pass


class MovieLensCSVSeeder(object):

    def __init__(self):
        self.items = db.items
        self.users = db.users
        self.ratings = db.ratings

    def seed_items(self):
        csv_items = pd.read_csv('storage/ml-20m/movies.csv', sep=',', encoding='latin1')
        self.items.insert_many(json.loads(csv_items.to_json(orient='records')))
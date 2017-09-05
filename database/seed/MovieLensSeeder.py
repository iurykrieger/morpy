from database.db import db
import pandas as pd
import json


class MovieLensSeeder(object):

    def __init__(self):
        self.items = db.items
        self.users = db.users
        self.ratings = db.ratings

    def seed_items(self):
        attrs = [
            'id',
            'title',
            'release_date',
            'video_release_date',
            'imdb_url',
            'unkwn',
            'action',
            'adventure',
            'animation',
            'children',
            'comedy',
            'crime',
            'documentary',
            'drama',
            'fantasy',
            'film-noir',
            'horror',
            'musical',
            'mystery',
            'romance',
            'sci-fi',
            'thriller',
            'war',
            'western'
        ]
        items = pd.read_csv('storage/ml-100k/u.item', sep='|', names=attrs, encoding='latin1')
        self.items.insert_many(json.loads(items.to_json(orient='records')))

    def seed_users(self):
        pass

    def seed_ratings(self):
        pass

import pandas as pd
import time
import redis
from flask import current_app
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from database.db import db
from app.common.exceptions import StatusCodeException
from Engine import Engine


def info(msg):
    current_app.logger.info(msg)


class ContentEngine(Engine):
    def __init__(self):
        self.items = db.items

    def _prepare(self):
        return pd.DataFrame(list(self.items.find()))[:2000]

    def _calculate(self, data):
        tfidf = TfidfVectorizer(
            analyzer='word',
            ngram_range=(1, 3),
            min_df=0,
            stop_words='english')
        tfidf_matrix = tfidf.fit_transform(data['title'])
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

        for index, row in data.iterrows():
            similar_indices = cosine_similarities[index].argsort()[:-100:-1]
            similar_items = [(cosine_similarities[index][i], data['id'][i])
                             for i in similar_indices]

            # First item is the item itself, so remove it.
            similar_items = similar_items[1:]

            similar_items = [{
                'id': item,
                'similarity': similarity
            } for similarity, item in similar_items]

            self._update(row, similar_items)

    def _update(self, item, similars=[]):
        self.items.find_one_and_update({
            'id': item['id']
        }, {'$set': {
            'similar': similar_items
        }})

    def train(self):
        """
        Train the engine.

        Create a TF-IDF matrix of unigrams, bigrams, and trigrams for each product. The 'stop_words' param
        tells the TF-IDF module to ignore common english words like 'the', etc.

        Then we compute similarity between all products using SciKit Leanr's linear_kernel (which in this case is
        equivalent to cosine similarity).

        Iterate through each item's similar items and store the 100 most-similar. Stops at 100 because well...
        how many similar products do you really need to show?
        Similarities and their scores are stored in redis as a Sorted Set, with one set for each item.

        :return: Nothin!
        """
        start = time.time()
        data = self._prepare()
        info("Training data ingested in %s seconds." % (time.time() - start))

        start = time.time()
        self._calculate(data)
        info("Engine trained in %s seconds." % (time.time() - start))
        return {'success': True}


content_engine = ContentEngine()

import pandas as pd
import time
import redis
from flask import current_app
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from database.db import db
from app.common.exceptions import StatusCodeException


def info(msg):
    current_app.logger.info(msg)


class ContentEngine(object):

    SIMKEY = 'p:smlr:%s'

    def __init__(self):
        self.items = db.test_items

    def train(self):
        start = time.time()
        ds = pd.DataFrame(list(self.items.find()))
        info("Training data ingested in %s seconds." % (time.time() - start))

        start = time.time()
        trained = self._train(ds)
        info("Engine trained in %s seconds." % (time.time() - start))
        return trained

    def _train(self, ds):
        """
        Train the engine.

        Create a TF-IDF matrix of unigrams, bigrams, and trigrams for each product. The 'stop_words' param
        tells the TF-IDF module to ignore common english words like 'the', etc.

        Then we compute similarity between all products using SciKit Leanr's linear_kernel (which in this case is
        equivalent to cosine similarity).

        Iterate through each item's similar items and store the 100 most-similar. Stops at 100 because well...
        how many similar products do you really need to show?

        Similarities and their scores are stored in redis as a Sorted Set, with one set for each item.

        :param ds: A pandas dataset containing two fields: description & id
        :return: Nothin!
        """
        tf = TfidfVectorizer(analyzer='word', ngram_range=(
            1, 3), min_df=0, stop_words='english')
        tfidf_matrix = tf.fit_transform(ds['description'])

        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

        ot = []
        for idx, row in ds.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
            similar_items = [(cosine_similarities[idx][i], ds['id'][i])
                             for i in similar_indices]

            # First item is the item itself, so remove it.
            # This 'sum' is turns a list of tuples into a single tuple: [(1,2), (3,4)] -> (1,2,3,4)
            # flattened = sum(, ())
            similar_items = [{
                'id': item,
                'similarity': similarity
            } for similarity, item in similar_items[1:]]

            self.items.find_one_and_update(
                {'id': row['id']},
                {'$set': {'similar': similar_items}}
            )

        return {'success': True}

    def recommend(self, item_id, number_of_recommendations=10):
        """
        Couldn't be simpler! Just retrieves the similar items and their 'score' from redis.

        :param item_id: int
        :param number_of_recommendations: number of similar items to return
        :return: A list of lists like: [["19", 0.2203], ["494", 0.1693], ...]. The first item in each sub-list is
        the item ID and the second is the similarity score. Sorted by similarity score, descending.
        """
        item = self.items.find_one({'id': item_id})
        if item:
            return item['similar'][:number_of_recommendations]
        else:
            raise StatusCodeException('No item found', 404)

content_engine = ContentEngine()

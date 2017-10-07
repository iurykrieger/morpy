"""
.. module:: project_documentation
    :platform: OS X
    :synopsis: module illustrating how to document python source code
 
.. moduleauthor:: Patrick Kennedy <patkennedy79@gmail.com>
"""

import pandas as pd
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from app.common.logging import info
from app.api.services.ItemService import ItemService


class ContentEngine(object):
    def __init__(self):
        start = time.time()
        self.item_service = ItemService()
        self.data = pd.DataFrame(list(self.item_service.get_rec_data()))
        self.tfidf = TfidfVectorizer(
            analyzer='word',
            ngram_range=(1, 3),
            min_df=0,
            smooth_idf=False,
            stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(
            self.data['concated_attrs'])
        self.cosine_similarities = linear_kernel(
            self.tfidf_matrix, self.tfidf_matrix)
        info("Training data ingested in %s seconds." % (time.time() - start))

    def _get_item_index(self, item_id):
        for index, item in self.data.iterrows():
            if item['_id'] == item_id:
                return item, index

    def _train_item(self, item, index):
        similar_indices = self.cosine_similarities[index].argsort()[:-50:-1]
        recs = [(self.cosine_similarities[index][similar_item], self.data['_id'][similar_item])
                for similar_item in similar_indices]

        recs = [
            {
                '_id': item_id,
                'similarity': similarity
            } for similarity, item_id in recs[1:]  # First item is the item itself, so remove it.
        ]

        self.item_service.update_recommendations(item['_id'], recs)

    def _train(self):
        for index, item in self.data.iterrows():
            self._train_item(item, index)

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
        self._train()
        info("Engine trained in %s seconds." % (time.time() - start))

    def train_item(self, item_id):
        start = time.time()
        item, index = self._get_item_index(item_id)
        self._train_item(item, index)
        info("Item %s trained in %s seconds." %
             (item_id, (time.time() - start)))

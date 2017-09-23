import pandas as pd
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction import DictVectorizer
from app.common.exceptions import StatusCodeException
from app.common.logging import info
from Engine import Engine
from app.api.metadata.ItemMetadata import ItemMetadata
import itertools


class ContentEngine(Engine):
    def __init__(self, db):
        self.items = db.items
        self.item_meta = ItemMetadata(
            db.item_metadata.find_one({'active': True}))
        self.data = []
        self.tfidf = TfidfVectorizer(
            analyzer='word',
            ngram_range=(1, 3),
            min_df=0,
            smooth_idf=False,
            stop_words='english')

    def _get_recommendable_attributes(self):
        return [attribute['name'] for attribute in self.item_meta.attributes if attribute['recommendable']]

    def _get_data_filter(self):
        attributes = self._get_recommendable_attributes()
        attribute_filter = {'$project': {}}
        concat_filter = {'$project': {}}

        for attr in attributes:
            attribute_filter['$project'][attr] = { '$ifNull': ['${name}'.format(name=attr), '']}
        
        concat_filter['$project']['concated_attrs'] = {'$concat': ['${name}'.format(name=attr) for attr in attributes]}
        
        return [attribute_filter, concat_filter]

    def _prepare(self):
        self.data = pd.DataFrame(list(self.items.aggregate(self._get_data_filter())))
        print self.data['concated_attrs']
        self.tfidf_matrix = self.tfidf.fit_transform(
            self.data['concated_attrs'])
        self.cosine_similarities = linear_kernel(
            self.tfidf_matrix, self.tfidf_matrix)

    def _get_item_index(self, item_id):
        for index, item in self.data.iterrows():
            if item['_id'] == item_id:
                return item, index

    def _train_item(self, item, index):
        similar_indices = self.cosine_similarities[index].argsort()[:-50:-1]
        similar_items = [(self.cosine_similarities[index][similar_item], self.data['_id'][similar_item])
                         for similar_item in similar_indices]

        # First item is the item itself, so remove it.
        similar_items = similar_items[1:]

        similar_items = [{
            '_id': item_id,
            'similarity': similarity
        } for similarity, item_id in similar_items]

        self._update(item, similar_items)

    def _train(self):
        for index, item in self.data.iterrows():
            self._train_item(item, index)

    def _update(self, item, similar):
        self.items.find_one_and_update({
            '_id': item['_id']
        }, {'$set': {
            'similar': similar
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
        self._prepare()
        info("Training data ingested in %s seconds." % (time.time() - start))

        start = time.time()
        self._train()
        info("Engine trained in %s seconds." % (time.time() - start))

    def train_item(self, item_id):
        start = time.time()
        self._prepare()
        info("Training data ingested in %s seconds." % (time.time() - start))

        start = time.time()
        item, index = self._get_item_index(item_id)
        self._train_item(item, index)
        info("Item %s trained in %s seconds." %
             (item_id, (time.time() - start)))

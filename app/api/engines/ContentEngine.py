# -*- coding: utf-8 -*-
"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

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

    def train(self):
        """
        Train the engine.

        Create a TF-IDF matrix of unigrams, bigrams, and trigrams for each product.

        Then similarity is computed between all products using SciKit Cosine Similarity.

        Iterate through each item's similar items and store the 50 most-similar.
        Similarities and their scores are stored in database as a sorted set, with one set for each item.

        :return: None
        """
        start = time.time()
        for index, item in self.data.iterrows():
            self._train_item(item, index)
        info("Engine trained in %s seconds." % (time.time() - start))

    def train_item(self, item_id):
        """
        Train the engine for a given item.

        Create a TF-IDF matrix of unigrams, bigrams, and trigrams for the given item.

        Then similarity is computed between the given product and all other products, using SciKit Cosine Similarity.

        Iterate through each item's similar items and store the 50 most-similar.
        Similarities and their scores are stored in database as a sorted set of the item.

        :return: None
        """
        start = time.time()
        item, index = self._get_item_index(item_id)
        self._train_item(item, index)
        info("Item %s trained in %s seconds." %
             (item_id, (time.time() - start)))

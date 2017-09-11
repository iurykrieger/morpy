
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
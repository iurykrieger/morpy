import abc


class Recommender(object):
    @abc.abstractmethod
    def recommend(self, *args):
        return
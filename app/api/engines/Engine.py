import abc


class Engine(object):
    @abc.abstractmethod
    def _prepare(self):
        return

    @abc.abstractmethod
    def _calculate(self, data):
        return

    @abc.abstractmethod
    def train(self):
        return

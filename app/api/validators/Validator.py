import abc

class Validator(object):

    def __init__(self, **args):
        return

    @abc.abstractmethod
    def validate(self):
        return
from app.api.engines.CollaborativeEngine import CollaborativeEngine
from multiprocessing import Process


class CollaborativeWorker(object):

    def _start_process(self, target, args):
        process = Process(target=target, args=args)
        process.daemon = True
        process.start()

    def train(self):
        self._start_process(CollaborativeEngine().train, ())

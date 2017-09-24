from app.api.engines.ContentEngine import ContentEngine
from multiprocessing import Process


class ContentWorker(object):

    def _start_process(self, target, args):
        process = Process(target=target, args=args)
        process.daemon = True
        process.start()

    def train_item(self, item_id):
        self._start_process(ContentEngine().train_item, (item_id, ))

    def train(self):
        self._start_process(ContentEngine().train, ())

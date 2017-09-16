from app.api.engines.ContentEngine import ContentEngine
from app.common.process import AbstractProcess
from database import db
from multiprocessing import Process


class ContentWorker(object):

    def __init__(self):
        self.engine = ContentEngine(db.get_db())

    def _start_process(self, target, args):
        process = Process(target=target, args=args)
        process.daemon = True
        process.start()

    def train_item(self, item_id):
        self._start_process(self.engine.train_item, (item_id, ))

    def train(self):
        self._start_process(self.engine.train, ())

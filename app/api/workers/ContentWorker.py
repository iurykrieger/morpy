from app.api.engines.ContentEngine import ContentEngine
from app.common.process import AbstractProcess
from database import db
from multiprocessing import Process


class ContentWorker(object):

    def train_item(self, item_id):
        process = Process(target=ContentEngine(db.get_db()).train_item, args=(item_id, ))
        process.daemon = True  # Daemonize it
        process.start()

    def train(self):
        process = Process(target=ContentEngine(db.get_db()).train, args=())
        process.daemon = True  # Daemonize it
        process.start()

    def _train_item(self, item_id):
        ContentEngine(db.get_db()).train_item(item_id)

    def _train(self):
        ContentEngine(db.get_db()).train()

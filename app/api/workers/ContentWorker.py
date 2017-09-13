from app.api.engines.ContentEngine import ContentEngine
from app.common.process import AbstractProcess
from database import db


class ContentWorker(AbstractProcess):
    def run(self):
        ContentEngine(db.get_db()).train()
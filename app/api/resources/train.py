# -*- coding: utf-8 -*-
from flask_restful import Resource
from app.common.exceptions import StatusCodeException
from app.common.auth import auth
from app.api.workers.ContentWorker import ContentWorker


class TrainItem(Resource):

    @auth.middleware_auth_token
    def get(self, item_id):
        try:
            ContentWorker().train_item(item_id)
            return {'status': 'training...'}
        except StatusCodeException as ex:
            return ex.to_response()


class Train(Resource):
    @auth.middleware_auth_token
    def get(self):
        try:
            ContentWorker().train()
            return {'status': 'training...'}
        except StatusCodeException as ex:
            return ex.to_response()

# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import request, make_response
from app.api.models.ItemModel import ItemModel
from app.common.exceptions import StatusCodeException
from app.common.auth import auth
from app.api.services.ItemService import ItemService
from app.api.workers.ContentWorker import ContentWorker


class Item(Resource):

    ENDPOINT = '/item/<objectid:item_id>'

    def __init__(self):
        self.item_service = ItemService()

    @auth.middleware_auth_token
    def get(self, item_id):
        try:
            item = self.item_service.get_by_id(item_id)
            if item:
                return make_response(ItemModel(item).to_json())
            else:
                raise StatusCodeException('Item not found', 404)
        except StatusCodeException as ex:
            return ex.to_response()
        except Exception as ex:
            return StatusCodeException(ex.message, 500).to_response()

    @auth.middleware_auth_token
    def delete(self, item_id):
        try:
            if self.item_service.get_by_id(item_id):
                self.item_service.remove(item_id)
                return make_response()
            else:
                raise StatusCodeException('Item not found', 404)
        except StatusCodeException as ex:
            return ex.to_response()
        except Exception as ex:
            return StatusCodeException(ex.message, 500).to_response()


class Items(Resource):

    ENDPOINT = '/item'

    def __init__(self):
        self.item_service = ItemService()

    @auth.middleware_auth_token
    def get(self):
        all_items = self.item_service.get_all()
        return make_response([ItemModel(item).to_json() for item in all_items])

    @auth.middleware_auth_token
    def post(self):
        try:
            item = ItemModel(request.get_json())
            if item.validate():
                item_id = self.item_service.insert(item.to_database())
                item.set_id(item_id)
                ContentWorker().train_item(item_id)
                return make_response(item.to_json())
            else:
                raise StatusCodeException('Conflict', 409)
        except StatusCodeException as ex:
            return ex.to_response()
        except Exception as ex:
            return StatusCodeException(ex.message, 500).to_response()

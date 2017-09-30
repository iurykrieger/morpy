# -*- coding: utf-8 -*-
from flask_restful import Resource
<<<<<<< HEAD
from flask import request, make_response, jsonify
from database.db import db, ObjectIDConverter
from app.common.exceptions import StatusCodeException
from app.common.auth import auth
from bson.json_util import loads, dumps
from app.api.metadata.ItemMetadata import ItemMetadata
from app.api.validators.ItemValidator import ItemValidator
=======
from flask import request, make_response
from app.api.models.ItemModel import ItemModel
from app.common.exceptions import StatusCodeException
from app.common.auth import auth
from app.api.services.ItemService import ItemService

>>>>>>> af8dd5f8dd191a6c8ad09a3f2dcc8dbe8453512e

class Item(Resource):

    ENDPOINT = '/item/<objectid:item_id>'

    def __init__(self):
        self.item_service = ItemService()

    @auth.middleware_auth_token
    def get(self, item_id):
        try:
<<<<<<< HEAD
            item = self.items.find_one(
                {'_id': item_id},
                {'similar': 0})
            meta = ItemMetadata(self.meta.find_one({"active": True}))
            validator = ItemValidator(meta, item)

            if validator.validate():
                item['_id'] = ObjectIDConverter.to_url(item['_id'])
                return make_response(item)
=======
            item = self.item_service.get_by_id(item_id)
            if item:
                return make_response(ItemModel(item).to_json())
            else:
                raise StatusCodeException('Item not found', 404)
        except StatusCodeException as ex:
            return ex.to_response()

    @auth.middleware_auth_token
    def delete(self, item_id):
        try:
            if self.item_service.get_by_id(item_id):
                self.item_service.remove(item_id)
                return make_response()
            else:
                raise StatusCodeException('Item not found', 404)
>>>>>>> af8dd5f8dd191a6c8ad09a3f2dcc8dbe8453512e
        except StatusCodeException as ex:
            return ex.to_response()


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
            item = request.get_json()
            if '_id' not in item:  # XXX - Compare unique metadata values
                item['_id'] = self.item_service.insert(item)
                return make_response(item)
            else:
                raise StatusCodeException('Conflict', 409)
        except StatusCodeException as ex:
            return ex.to_response()

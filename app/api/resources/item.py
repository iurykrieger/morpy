# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import request, make_response, jsonify
from database.db import db, ObjectIDConverter
from app.api.models.user import User as UserModel
from app.api.models.ItemModel import ItemModel
from app.common.exceptions import StatusCodeException
from app.common.auth import auth
from bson.json_util import loads, dumps
from app.api.metadata.ItemMetadata import ItemMetadata

class Item(Resource):

    ENDPOINT = '/item/<objectid:item_id>'

    def __init__(self):
        self.items = db.items
        self.meta = db.item_metadata

    @auth.middleware_auth_token
    def get(self, item_id):
        try:
            item = self.items.find_one(
                {'_id': item_id},
                {'similar': 0})
            item = ItemModel(item)
            return make_response(item.to_json())
        except StatusCodeException as ex:
            return ex.to_response()


class Items(Resource):

    ENDPOINT = '/item'

    def __init__(self):
        self.items = db.items

    @auth.middleware_auth_token
    def get(self):
        all_items = self.items.find({}, {'similar': 0})
        json_items = [ItemModel(item).to_json() for item in all_items]
        return make_response(json_items)

    @auth.middleware_auth_token
    def post(self):
        try:
            item = request.get_json()
            if '_id' not in item: # XXX - Compare unique metadata values
                item['_id'] = ObjectIDConverter.to_url(self.items.insert(item))
                return make_response(item)
            else:
                raise StatusCodeException('Conflict', 409)
        except StatusCodeException as ex:
            return ex.to_response()

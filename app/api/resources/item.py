# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import request, make_response, jsonify
from database.db import db, ObjectIDConverter
from app.common.exceptions import StatusCodeException
from app.common.auth import auth
from bson.json_util import loads, dumps
from app.api.metadata.ItemMetadata import ItemMetadata
from app.api.validators.ItemValidator import ItemValidator

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
            meta = ItemMetadata(self.meta.find_one({"active": True}))
            validator = ItemValidator(meta, item)

            if validator.validate():
                item['_id'] = ObjectIDConverter.to_url(item['_id'])
                return make_response(item)
        except StatusCodeException as ex:
            return ex.to_response()


class Items(Resource):

    ENDPOINT = '/item'

    def __init__(self):
        self.items = db.items

    @auth.middleware_auth_token
    def get(self):
        all_items = self.items.find({}, {'similar': 0})
        items = []
        for item in all_items:
            item['_id'] = ObjectIDConverter.to_url(item['_id'])
            items.append(item)
        return make_response(items)

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

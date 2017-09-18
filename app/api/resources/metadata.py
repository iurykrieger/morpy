# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import request, make_response, jsonify
from database.db import db, ObjectIDConverter
from app.api.metadata.ItemMetadata import ItemMetadata
from app.api.metadata.UserMetadata import UserMetadata
from app.common.exceptions import StatusCodeException
from app.common.auth import auth
from bson.json_util import loads, dumps


class Metadata(Resource):

    ENDPOINT = '/metadata/<string:meta_type>'

    def __init__(self):
        self.item_meta = db.item_metadata
        self.user_meta = db.user_metadata

    @auth.middleware_auth_token
    def post(self, meta_type):
        try:
            if meta_type == 'item':
                collection = self.item_meta
                new_metadata = ItemMetadata(request.get_json())
            elif meta_type == 'user':
                collection = self.user_meta
                new_metadata = UserMetadata(request.get_json())
            else:
                raise StatusCodeException('Invalid type', 400)

            if not collection.find_one({'active': True}):
                collection.insert(new_metadata.to_database())
                return make_response(new_metadata.to_json())
            else:
                raise StatusCodeException('Conflict', 409)
        except StatusCodeException as ex:
            return ex.to_response()

    @auth.middleware_auth_token
    def put(self, type):
        try:
            if meta_type == 'item':
                collection = self.item_meta
                new_metadata = ItemMetadata(request.get_json())
            elif meta_type == 'user':
                collection = self.user_meta
                new_metadata = UserMetadata(request.get_json())
            else:
                raise StatusCodeException('Invalid type', 400)

            collection.find_and_update(
                {
                    'active': True
                }, {'$set': {
                    'active': False
                }}, {'$inc': {
                    'version': 1
                }},
                return_document=ReturnDocument.AFTER)

            if not collection.find_one({'active': True}):
                collection.insert(new_metadata.to_database())
                return make_response(new_metadata.to_json())
            else:
                raise StatusCodeException('Conflict', 409)
        except StatusCodeException as ex:
            return ex.to_response()

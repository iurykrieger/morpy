# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import request, make_response, jsonify
from database.db import db, ObjectIDConverter
from app.api.metadata.ItemMetadata import ItemMetadata
from app.api.metadata.UserMetadata import UserMetadata
from app.common.exceptions import StatusCodeException
from app.common.auth import auth
import pymongo

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
                new_metadata = ItemMetadata(request.get_json(), version=1, active=True)
            elif meta_type == 'user':
                collection = self.user_meta
                new_metadata = UserMetadata(request.get_json(), version=1, active=True)
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
    def put(self, meta_type):

        def _get_new_version(collection):
            old_meta = collection.find_one({'active': True})
            if old_meta:
                return old_meta['version'] + 1
            
            raise StatusCodeException('No metadata found for item.', 404)
                
        try:
            if meta_type == 'item':
                collection = self.item_meta
                new_metadata = request.get_json()
                new_metadata = ItemMetadata(new_metadata, _get_new_version(collection), True)
            elif meta_type == 'user':
                collection = self.user_meta
                new_metadata = request.get_json()
                new_metadata = UserMetadata(new_metadata, _get_new_version(collection), True)
            else:
                raise StatusCodeException('Invalid type', 400)

            collection.update({'active': True}, {'$set': {'active': False}})
            collection.insert(new_metadata.to_database())
            return make_response(new_metadata.to_json())

        except StatusCodeException as ex:
            return ex.to_response()


class MetadataList(Resource):

    ENDPOINT = '/metadata/<string:meta_type>/history'

    def __init__(self):
        self.item_meta = db.item_metadata
        self.user_meta = db.user_metadata

    @auth.middleware_auth_token
    def get(self, meta_type):
        try:
            if meta_type == 'item':
                json_metadata = [ItemMetadata(meta).to_json() 
                    for meta in self.item_meta.find().sort([('version', pymongo.DESCENDING)])]
            elif meta_type == 'user':
                json_metadata = [UserMetadata(meta).to_json()
                    for meta in self.user_meta.find().sort([('version', pymongo.DESCENDING)])]
            else:
                raise StatusCodeException('Invalid type', 400)

            return make_response(json_metadata)
        except StatusCodeException as ex:
            return ex.to_response()
# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import request, make_response, jsonify
from database.db import db, ObjectIDConverter
from app.api.metadata.ItemMetadata import ItemMetadata
from app.common.exceptions import StatusCodeException
from app.common.auth import auth
from bson.json_util import loads, dumps


class Metadata(Resource):

    ENDPOINT = '/metadata/<string:type>'

    def __init__(self):
        self.item_meta = db.item_metadata

    @auth.middleware_auth_token
    def post(self, type):
        try:
            new_metadata = ItemMetadata(request.get_json())
            if not self.item_meta.find_one({'active': True}):
                self.item_meta.insert(new_metadata.to_database())
                return make_response(new_metadata.to_json())
            else:
                raise StatusCodeException('Conflict', 409)
        except StatusCodeException as ex:
            return ex.to_response()

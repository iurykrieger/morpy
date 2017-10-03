# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import request, make_response
from app.api.metadata.ItemMetadata import ItemMetadata
from app.api.metadata.UserMetadata import UserMetadata
from app.common.exceptions import StatusCodeException
from app.common.auth import auth
from app.api.services.ItemMetadataService import ItemMetadataService
from app.api.services.UserMetadataService import UserMetadataService

class Metadata(Resource):

    ENDPOINT = '/metadata/<string:meta_type>'

    def __init__(self):
        self.item_meta_service = ItemMetadataService()
        self.user_meta_service = UserMetadataService()

    @auth.middleware_auth_token
    def post(self, meta_type):
        try:
            if meta_type == 'item':
                service = self.item_meta_service
                new_metadata = ItemMetadata(request.get_json(), version=1, active=True)
            elif meta_type == 'user':
                service = self.user_meta_service
                new_metadata = UserMetadata(request.get_json(), version=1, active=True)
            else:
                raise StatusCodeException('Invalid type', 400)

            if not service.get_active():
                service.insert(new_metadata.to_database())
                return make_response(new_metadata.to_json())
            else:
                raise StatusCodeException('Conflict', 409)
        except StatusCodeException as ex:
            return ex.to_response()
        except Exception as ex:
            return StatusCodeException(ex.message, 500).to_response()

    @auth.middleware_auth_token
    def put(self, meta_type):

        def _get_new_version(service):
            meta = service.get_active()
            if meta:
                return meta['version'] + 1

            raise StatusCodeException('Item metadata not found', 404)

        try:
            if meta_type == 'item':
                service = self.item_meta_service
                new_metadata = request.get_json()
                new_metadata = ItemMetadata(new_metadata, _get_new_version(service), True)
            elif meta_type == 'user':
                service = self.user_meta_service
                new_metadata = request.get_json()
                new_metadata = UserMetadata(new_metadata, _get_new_version(service), True)
            else:
                raise StatusCodeException('Invalid type', 400)

            service.disable_all()
            service.insert(new_metadata.to_database())
            return make_response(new_metadata.to_json())

        except StatusCodeException as ex:
            return ex.to_response()
        except Exception as ex:
            return StatusCodeException(ex.message, 500).to_response()


class MetadataList(Resource):

    ENDPOINT = '/metadata/<string:meta_type>/history'

    def __init__(self):
        self.item_meta_service = ItemMetadataService()
        self.user_meta_service = UserMetadataService()

    @auth.middleware_auth_token
    def get(self, meta_type):
        try:
            if meta_type == 'item':
                json_metadata = [ItemMetadata(meta).to_json()
                    for meta in self.item_meta_service.get_all()]
            elif meta_type == 'user':
                json_metadata = [UserMetadata(meta).to_json()
                    for meta in self.user_meta_service.get_all()]
            else:
                raise StatusCodeException('Invalid type', 400)

            return make_response(json_metadata)
        except StatusCodeException as ex:
            return ex.to_response()
        except Exception as ex:
            return StatusCodeException(ex.message, 500).to_response()
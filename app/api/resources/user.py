# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import request, make_response
<<<<<<< HEAD
from pymongo import ReturnDocument
from database.db import db
=======
from app.api.services.UserService import UserService
from app.api.models.UserModel import UserModel
>>>>>>> af8dd5f8dd191a6c8ad09a3f2dcc8dbe8453512e
from app.common.exceptions import StatusCodeException
from app.common.auth import auth


class User(Resource):

    ENDPOINT = '/user/<objectid:user_id>'

    def __init__(self):
        self.service = UserService()

    @auth.middleware_auth_token
    def get(self, user_id):
        try:
            user = self.service.get_by_id(user_id)
            user = UserModel(user)
            return make_response(user.to_json())
        except StatusCodeException as ex:
            return ex.to_response()

    @auth.middleware_auth_token
    def put(self, user_id):
        try:
            user = self.service.update(user_id, request.get_json())
            if user:
                user = UserModel(user)
                return make_response(user.to_json())
            else:
                raise StatusCodeException('User not found', 404)
        except StatusCodeException as ex:
            return ex.to_response()

    @auth.middleware_auth_token
    def delete(self, user_id):
        try:
            if self.service.get_by_id(user_id):
                self.service.remove(user_id)
                return make_response()
            else:
                raise StatusCodeException('User not found', 404)
        except StatusCodeException as ex:
            return ex.to_response()


class Users(Resource):
    
    ENDPOINT = '/user'

    def __init__(self):
        self.service = UserService()

    @auth.middleware_auth_token
    def get(self):
        all_users = self.service.get_all()
        json_users = [UserModel(user).to_json() for user in all_users]
        return make_response(json_users)

    def post(self):
        try:
            user = request.get_json()
            if not False:
                user['_id'] = self.service.insert(user)
                return make_response(user)
            else:
                raise StatusCodeException('Conflict', 409)
        except StatusCodeException as ex:
            return ex.to_response()

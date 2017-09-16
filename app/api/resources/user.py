# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import request, make_response
from pymongo import ReturnDocument
from database.db import db
from app.api.models.user import User as UserModel
from app.common.exceptions import StatusCodeException
from app.common.auth import auth


class User(Resource):
    
    ENDPOINT = '/user/<objectid:user_id>'

    def __init__(self):
        self.users = db.users

    @auth.middleware_auth_token
    def get(self, user_id):
        try:
            user = self.users.find_one(user_id)
            user = UserModel(user)
            return make_response(user.to_json())
        except StatusCodeException as ex:
            return ex.to_response()

    @auth.middleware_auth_token
    def put(self, user_id):
        try:
            user_info = request.get_json()
            user = self.users.find_one_and_update(
                {'_id': user_id},
                {'$set': {
                    'name': user_info['name'],
                    'age': user_info['age'],
                    'email': user_info['email']
                }},
                return_document=ReturnDocument.AFTER
            )
            if user:
                user = UserModel(user)
                return make_response(user.to_json())
            else:
                raise StatusCodeException('User not found', 404)
        except StatusCodeException as ex:
            return ex.to_response()


class Users(Resource):
    
    ENDPOINT = '/user'

    def __init__(self):
        self.users = db.users

    @auth.middleware_auth_token
    def get(self):
        output = []
        all_users = self.users.find({'email': {'$exists': True}})
        for user in all_users:
            user = UserModel(user)
            output.append(user.to_json())
        return make_response({'users': output})

    def post(self):
        try:
            user = UserModel(request.get_json())
            if not self.users.find_one({'email': user.email}):
                user._id = self.users.insert(user.to_database())
                return make_response(user.to_json())
            else:
                raise StatusCodeException('Conflict', 409)
        except StatusCodeException as ex:
            return ex.to_response()

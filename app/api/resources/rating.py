# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import request, make_response
from app.api.services.RatingService import RatingService
from app.api.models.RatingModel import RatingModel
from app.common.exceptions import StatusCodeException
from app.common.auth import auth


class Rating(Resource):

    ENDPOINT = '/rating/<objectid:rating_id>'

    def __init__(self):
        self.service = RatingService()

    @auth.middleware_auth_token
    def get(self, rating_id):
        try:
            rating = self.service.get_by_id(rating_id)
            rating = RatingModel(rating)
            return make_response(rating.to_json())
        except StatusCodeException as ex:
            return ex.to_response()
        except Exception as ex:
            return StatusCodeException(ex.message, 500).to_response()

    @auth.middleware_auth_token
    def put(self, rating_id):
        try:
            rating = self.service.update(rating_id, request.get_json())
            if rating:
                rating = RatingModel(rating)
                return make_response(rating.to_json())
            else:
                raise StatusCodeException('Rating not found', 404)
        except StatusCodeException as ex:
            return ex.to_response()
        except Exception as ex:
            return StatusCodeException(ex.message, 500).to_response()

    @auth.middleware_auth_token
    def delete(self, rating_id):
        try:
            if self.service.get_by_id(rating_id):
                self.service.remove(rating_id)
                return make_response()
            else:
                raise StatusCodeException('Rating not found', 404)
        except StatusCodeException as ex:
            return ex.to_response()
        except Exception as ex:
            return StatusCodeException(ex.message, 500).to_response()


class Ratings(Resource):

    ENDPOINT = '/rating'

    def __init__(self):
        self.service = RatingService()

    @auth.middleware_auth_token
    def get(self):
        all_ratings = self.service.get_all()
        json_ratins = [RatingModel(rating).to_json() for rating in all_ratings]
        return make_response(json_ratins)

    def post(self):
        try:
            rating = request.get_json()
            if not False: # XXX - Metadata validation here!
                rating['_id'] = self.service.insert(rating)
                return make_response(rating)
            else:
                raise StatusCodeException('Conflict', 409)
        except StatusCodeException as ex:
            return ex.to_response()
        except Exception as ex:
            return StatusCodeException(ex.message, 500).to_response()

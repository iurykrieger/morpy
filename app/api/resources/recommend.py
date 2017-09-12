from flask_restful import Resource
from flask import request, make_response
from app.common.exceptions import StatusCodeException
from app.common.auth import auth
from app.api.recommenders.ContentRecommender import content_recommender

class Recommend(Resource):

    def __init__(self):
        pass

    @auth.middleware_auth_token
    def get(self, item_id, number_of_recommendations=10):
        try:
            return make_response(content_recommender.recommend(item_id, number_of_recommendations))
        except StatusCodeException as ex:
            return ex.to_response()
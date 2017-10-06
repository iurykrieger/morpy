from flask_restful import Resource
from flask import make_response
from app.common.exceptions import StatusCodeException
from app.common.auth import auth
from app.api.services.RecommenderService import RecommenderService

class Recommend(Resource):

    ENDPOINT = '/recommend/<objectid:item_id>/top/<int:number_of_recommendations>'

    def __init__(self):
        self.recommender_service = RecommenderService()

    @auth.middleware_auth_token
    def get(self, item_id, number_of_recommendations=10):
        try:
            return make_response(self.recommender_service.recommend(item_id, end=number_of_recommendations))
        except StatusCodeException as ex:
            return ex.to_response()
        except Exception as ex:
            return StatusCodeException(ex.message, 500).to_response()

class RecommendPagination(Resource):

    ENDPOINT = '/recommend/<objectid:item_id>/<int:start>/<int:end>'

    def __init__(self):
        self.recommender_service = RecommenderService()

    @auth.middleware_auth_token
    def get(self, item_id, start, end):
        try:
            return make_response(self.recommender_service.recommend(item_id, start, end))
        except StatusCodeException as ex:
            return ex.to_response()
        except Exception as ex:
            return StatusCodeException(ex.message, 500).to_response()
# -*- coding: utf-8 -*-
from flask_api import FlaskAPI
from flask import request
from flask_restful import Api
from database.db import ObjectIDConverter
from routes import ROUTES
from api.resources.users import Users, User
from api.resources.token import Token
from api.resources.recommend import Recommend

from api.engines.ContentEngine import content_engine

# Global defines
app = FlaskAPI(__name__)
app.config.from_pyfile('../settings.py')
app.url_map.converters['objectid'] = ObjectIDConverter
api = Api(app)

api.add_resource(Token, '/token', endpoint='token')
api.add_resource(User, '/users/<objectid:user_id>', endpoint='user')
api.add_resource(Users, '/users', endpoint='users')
api.add_resource(
    Recommend,
    '/recommend/<int:item_id>/top/<int:number_of_recommendations>',
    endpoint='recommend')


@app.route('/', methods=['GET'])
def root():
    return ROUTES


@app.route('/train', methods=['GET'])
def train():
    return content_engine.train()

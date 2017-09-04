# -*- coding: utf-8 -*-
from flask_api import FlaskAPI
from flask import request
from flask_restful import Api
from database.db import ObjectIDConverter
from routes import ROUTES
from api.resources.users import Users, User
from api.resources.token import Token
from api.resources.recommend import Recommend

from api.engines.tfidf import content_engine


# Global defines
app = FlaskAPI(__name__)
app.config.from_pyfile('../settings.py')
app.url_map.converters['objectid'] = ObjectIDConverter
api = Api(app)

api.add_resource(Token, '/token', endpoint='token')
api.add_resource(User, '/users/<objectid:user_id>', endpoint='user')
api.add_resource(Users, '/users', endpoint='users')
api.add_resource(Recommend, '/recommend/<int:item_id>/<int:number_of_recommendations>', endpoint='recommend')


@app.route('/', methods=['GET'])
def root():
    return ROUTES


@app.route('/train', methods=['GET'])
def train():
    return content_engine.train()

"""
@app.route(ROUTES['predict']['endpoint'], methods=ROUTES['predict']['methods'])
@auth.middleware_auth_token
def predict():
    from engines import content_engine
    item = request.data.get('item')
    num_predictions = request.data.get('num', 10)
    if not item:
        return []
    return content_engine.predict(str(item), num_predictions)


@app.route(ROUTES['train']['endpoint'], methods=ROUTES['train']['methods'])
@auth.middleware_auth_token
def train():
    from engines import content_engine
    data_url = request.data.get('data-url', None)
    content_engine.train('storage/%s' % data_url)
    return {"message": "Success!", "success": 1}
"""

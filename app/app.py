# -*- coding: utf-8 -*-
from flask_api import FlaskAPI
from flask_restful import Api
from database.db import ObjectIDConverter
from api.resources.user import Users, User
from api.resources.token import Token
from api.resources.recommend import Recommend
from api.resources.train import TrainItem, Train
from api.resources.item import Items, Item

# Global defines
app = FlaskAPI(__name__)
app.config.from_pyfile('../settings.py')
app.url_map.converters['objectid'] = ObjectIDConverter
api = Api(app)

api.add_resource(Token, Token.ENDPOINT, endpoint='token')
api.add_resource(User, User.ENDPOINT, endpoint='user')
api.add_resource(Users, Users.ENDPOINT, endpoint='users')
api.add_resource(Recommend, Recommend.ENDPOINT, endpoint='recommend')
api.add_resource(Train, Train.ENDPOINT, endpoint='train')
api.add_resource(TrainItem, TrainItem.ENDPOINT, endpoint='train_item')
api.add_resource(Items, Items.ENDPOINT, endpoint='items')
api.add_resource(Item, Item.ENDPOINT, endpoint='item')

@app.route('/', methods=['GET'])
def root():
    return {'status': 'running'}

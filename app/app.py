from flask_api import FlaskAPI
from flask import request, jsonify, abort
from flask_restful import Api
from common.auth import Auth
from common.exceptions import StatusCodeException
from database.db import ObjectIDConverter, db
from routes import ROUTES

from api.resources.users import Users, User


# Global defines
app = FlaskAPI(__name__)
app.config.from_pyfile('../settings.py')
app.url_map.converters['objectid'] = ObjectIDConverter
auth = Auth(app.config['SECRET_KEY'])
api = Api(app)

api.add_resource(User, '/users/<objectid:user_id>', endpoint='user')
api.add_resource(Users, '/users', endpoint='users')


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


@app.route('/token', methods=['POST'])
def token():
    email = request.data.get('email', None)
    password = request.data.get('password', None)
    if email and password:
        token = auth.generate_token(email, password)
        if token:
            return {'token': token}
        else:
            abort(404)
    else:
        abort(400)


@app.route(ROUTES['root']['endpoint'], methods=ROUTES['root']['methods'])
def root():
    return ROUTES
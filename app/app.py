from flask_api import FlaskAPI
from flask import request, jsonify, abort
from flask_pymongo import PyMongo
from common.auth import Auth
from common.mongo import ObjectIDConverter
from routes import ROUTES


# Global defines
app = FlaskAPI(__name__)
app.config.from_pyfile('../settings.py')
app.url_map.converters['objectid'] = ObjectIDConverter
auth = Auth(app.config['SECRET_KEY'])
PyMongo(app)


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


@app.route('/users', methods=['POST'])
def add_user():
    email = request.data.get('email', None)
    name = request.data.get('name', None)
    age = request.data.get('age', None)
    password = request.data.get('password', None)
    if email and name and age and password:
        from pymongo import MongoClient
        users = MongoClient().db.users
        user = users.find_one({'email': email, 'password': password})
        if not user:
            user_id = users.insert(
                {'email': email, 'name': name, 'age': age, 'password': password})
            user = users.find_one(user_id)
            return {'_id': '%r' % user['_id'], 'email': user['email'], 'name': user['name'], 'age': user['age']}
        else:
            abort(409)
    else:
        abort(400)


@app.route('/users/<objectid:user_id>', methods=['GET'])
def get_user(user_id):
    return {'user_id': '%s' % user_id}


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


@app.route('/users', methods=['GET'])
@auth.middleware_auth_token
def get_all_users():
    from pymongo import MongoClient
    mongo = MongoClient()
    users = mongo.db.user

    user_id = users.insert(
        {'name': 'Eloisa Renata Schons', 'sex': 'F', 'age': 18})

    output = []
    all_users = users.find()
    for user in all_users:
        output.append(
            {'nome': user['name'], 'sexo': user['sex'], 'idade': user['age']})

    return {'users': output}

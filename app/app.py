from flask.ext.api import FlaskAPI
from flask import request, current_app, abort, jsonify
from common.auth import middleware_auth_token
from routes import ROUTES
from flask_pymongo import PyMongo
from common import mongo

app = FlaskAPI(__name__)
app.config.from_pyfile('../settings.py')
mongo = PyMongo(app)
from mongokit import Connection

connection = Connection()

@app.route(ROUTES['predict']['endpoint'], methods=ROUTES['predict']['methods'])
@middleware_auth_token
def predict():
    from engines import content_engine
    item = request.data.get('item')
    num_predictions = request.data.get('num', 10)
    if not item:
        return []
    return content_engine.predict(str(item), num_predictions)


@app.route(ROUTES['train']['endpoint'], methods=ROUTES['train']['methods'])
@middleware_auth_token
def train():
    from engines import content_engine
    data_url = request.data.get('data-url', None)
    content_engine.train('storage/%s' % data_url)
    return {"message": "Success!", "success": 1}


@app.route(ROUTES['root']['endpoint'], methods=ROUTES['root']['methods'])
def root():
    return ROUTES


@app.route('/users', methods=['GET'])
def get_all_users():
    users = mongo.db.user

    user_id = users.insert({'name': 'Eloisa Renata Schons', 'sex': 'F', 'age': 18})

    output = []
    all_users = users.find()
    for user in all_users:
        output.append({'nome' : user['name'], 'sexo' : user['sex'], 'idade': user['age']})

    return {'usuarios': output}


@app.route('/user/<name>', methods=['GET'])
def get_user_by_bame(name):
    user = mongo.db.user

    u = user.find_one({'name': name})

    if u:
        output = {'name': u['name'], 'sex': u['sex'], 'age': u['age']}
    else:
        output = 'No results found'

    return jsonify({'result': output})


@app.route('/user', methods=['POST'])
def add_framework():
    users = mongo.db.users

    user_id = users.insert({'name': 'Eloisa Renata Schons', 'sex': 'F', 'age': 18})
    new_user = user.find_one({'_id': user_id})

    output = {'name': new_user['name'], 'sex': new_user['sex'], 'age': new_user['age']}

    return jsonify({'result': output})

@app.route('/token', methods=['GET'])
def token():
    users = mongo.get_db().users

    user_id = users.insert({'name': 'Eloisa Renata Schons', 'sex': 'F', 'age': 18})

    output = []
    all_users = users.find()
    for user in all_users:
        output.append({'nome' : user['name'], 'sexo' : user['sex'], 'idade': user['age']})

    return {'usuarios': output}
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb://iury:123456@127.0.0.1:27017/test'


@app.route('/user', methods=['GET'])
def get_all_users():
    user = mongo.db.user

    output = []

    for u in user.find():
        output.append({'name': u['name'], 'sex': u['sex'], 'age': u['age']})

    return jsonify({'result': output})


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
    user = mongo.db.user

    name = request.json['name']
    sex = request.json['sex']
    age = request.json['age']

    user_id = user.insert({'name': name, 'sex': sex, 'age': age})
    new_user = user.find_one({'_id': user_id})

    output = {'name': new_user['name'], 'sex': new_user['sex'], 'age': new_user['age']}

    return jsonify({'result': output})


mongo = PyMongo(app)

if __name__ == '__main__':
    app.run(debug=True)

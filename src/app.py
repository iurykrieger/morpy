from flask.ext.api import FlaskAPI
from flask import request, current_app, abort
from common.auth import middleware_auth_token
from routes import ROUTES

app = FlaskAPI(__name__)
app.config.from_object('src.settings')


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

# -*- coding: utf-8 -*-
# routes.py

ROUTES = {
    'root': {
        'endpoint': '/',
        'methods': ['GET'],
        'description': 'Returns all api routes.'
    },
    'train': {
        'endpoint': '/train',
        'methods': ['GET'],
        'description': 'Trains a given database to make future recommendations.'
    },
    'predict': {
        'endpoint': '/predict',
        'methods': ['POST'],
        'description': 'Returns recommendations based on a given user.'
    }
}

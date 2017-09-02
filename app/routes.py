# -*- coding: utf-8 -*-
# routes.py

ROUTES = {
    'root': {
        'endpoint': '/',
        'methods': ['GET'],
        'description': 'Returns all api routes.',
        'auth_required': False,
    },
    'token': {
        'endpoint': '/token',
        'methods': ['POST'],
        'description': 'Retrieves a token based on user sent.',
        'auth_required': False,
    },
    'train': {
        'endpoint': '/train',
        'methods': ['GET'],
        'description': 'Trains a given database to make future recommendations.',
        'auth_required': True,
    },
    'predict': {
        'endpoint': '/predict',
        'methods': ['POST'],
        'description': 'Returns recommendations based on a given user.',
        'auth_required': True,
    }
}

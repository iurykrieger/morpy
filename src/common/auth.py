from functools import wraps


def middleware_auth_token(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('token', None) != current_app.config['API_TOKEN']:
            abort(403)
        return function(*args, **kwargs)
    return decorated_function

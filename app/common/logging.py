from flask import current_app

def info(message):
    current_app.logger.info(message)
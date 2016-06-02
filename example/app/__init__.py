from flask import Flask
from flask_celery import Celery

celery = Celery(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    celery.init_app(app)

    from .test import test as test_blueprint
    app.register_blueprint(test_blueprint)

    return app

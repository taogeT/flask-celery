=============================
Flask Celery 3.0+ Integration
=============================
:Python: 3.4+
:Celery: 3.0.0+

Celery: http://celeryproject.org

Using Flask-Celery
==================

You can easily add Celery to your flask application like this:

``app.py``::

    from flask.ext.celery import Celery

    celery = Celery()

    def create_app():
        app = Flask(__name__)

        celery.init_app(app)

        return app

    @celery.task
    def add(x, y):
        return x + y

To start the worker you can then launch the ``celery worker`` command
by pointing to your ``celery`` app instance::

    $ celery -A app:celery worker -l info

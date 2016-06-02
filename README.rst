=============================
Flask Celery 3.0+ Integration
=============================
.. image:: https://img.shields.io/pypi/v/Flask-Celery-py3.svg
    :target: https://pypi.python.org/pypi/Flask-Celery-py3/
.. image:: https://img.shields.io/pypi/dm/Flask-Celery-py3.svg
    :target: https://pypi.python.org/pypi/Flask-Celery-py3/
.. image:: https://img.shields.io/pypi/l/Flask-Celery-py3.svg
    :target: https://pypi.python.org/pypi/Flask-Celery-py3
.. image:: https://img.shields.io/pypi/pyversions/Flask-Celery-py3.svg
    :target: https://pypi.python.org/pypi/Flask-Celery-py3/
.. image:: https://img.shields.io/pypi/status/Flask-Celery-py3.svg
    :target: https://pypi.python.org/pypi/Flask-Celery-py3/

Celery: http://celeryproject.org

Using Flask-Celery
==================

You can easily add Celery to your flask application like this:

``app.py``::

    from flask_celery import Celery

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

If your flask application has complex condition, you can refer to the example https://github.com/taogeT/flask-celery .

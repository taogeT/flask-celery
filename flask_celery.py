# -*- coding: UTF-8 -*-
from celery import Celery as _Celery

__all__ = ['Celery']


class _CeleryConfig(object):

    def __init__(self, celery):
        self.celery = celery


class Celery(_Celery):

    def __init__(self, app=None, **kwargs):
        super(Celery, self).__init__(**kwargs)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.conf.update(app.config)
        if app.config.get('CELERY_BROKER_URL', None):
            self.conf.update(BROKER_URL=app.config['CELERY_BROKER_URL'])
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['celery'] = _CeleryConfig(self)

# -*- coding: UTF-8 -*-
from celery import Celery as _Celery

__all__ = ['Celery']


class Celery(_Celery):

    def __init__(self, **kwargs):
        super(Celery, self).__init__(**kwargs)
        if 'app' in kwargs:
            self.init_app(kwargs['app'])

    def init_app(self, app):
        self.conf.update(app.config)
        if 'CELERY_BROKER_URL' in app.config:
            self.conf.update(BROKER_URL=app.config['CELERY_BROKER_URL'])
        if 'CELERY_ADMINS' in app.config:
            self.conf.update(ADMINS=app.config['CELERY_ADMINS'])

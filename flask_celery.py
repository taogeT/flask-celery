# -*- coding: UTF-8 -*-
from celery import Celery as _Celery
from celery.loaders.app import AppLoader

__all__ = ['Celery']


class Celery(_Celery):

    loader_cls = 'flask_celery:FlaskLoader'

    def __init__(self, *args, **kwargs):
        super(Celery, self).__init__(*args, **kwargs)
        self.flask_app = kwargs.get('flask_app', None)

    def init_app(self, flask_app):
        self.flask_app = flask_app
        self.conf.update(self.flask_app.config)
        if 'CELERY_BROKER_URL' in self.flask_app.config:
            self.conf.update(BROKER_URL=self.flask_app.config['CELERY_BROKER_URL'])
        if 'CELERY_ADMINS' in self.flask_app.config:
            self.conf.update(ADMINS=self.flask_app.config['CELERY_ADMINS'])
        blueprint_import = [iterbp.import_name for iterbp in self.flask_app.iter_blueprints()]
        self.autodiscover_tasks([self.flask_app.import_name] + blueprint_import)


class FlaskLoader(AppLoader):

    def __init__(self, app, **kwargs):
        super(FlaskLoader, self).__init__(app, **kwargs)
        self.flask_request_context = None

    def on_task_init(self, task_id, task):
        self.flask_request_context = self.app.flask_app.test_request_context()
        self.flask_request_context.push()

    def on_process_cleanup(self):
        self.flask_request_context.pop()

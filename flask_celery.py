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

        self.conf.update(BROKER_URL=self.flask_app.config.get('CELERY_BROKER_URL', ''))
        self.conf.update(ADMINS=self.flask_app.config.get('CELERY_ADMINS', ()))
        self.conf.update(SERVER_EMAIL=self.flask_app.config.get('CELERY_ADMINS', ''))
        self.conf.update(EMAIL_HOST=self.flask_app.config.get('CELERY_EMAIL_HOST', ''))
        self.conf.update(EMAIL_HOST_USER=self.flask_app.config.get('CELERY_EMAIL_HOST_USER', ''))
        self.conf.update(EMAIL_HOST_PASSWORD=self.flask_app.config.get('CELERY_EMAIL_HOST_PASSWORD', ''))
        self.conf.update(EMAIL_PORT=self.flask_app.config.get('CELERY_EMAIL_PORT', 25))
        self.conf.update(EMAIL_USE_SSL=self.flask_app.config.get('CELERY_EMAIL_USE_SSL', False))
        self.conf.update(EMAIL_USE_TLS=self.flask_app.config.get('CELERY_EMAIL_USE_TLS', False))

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

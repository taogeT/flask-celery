# -*- coding: UTF-8 -*-
from celery import Celery as _Celery
from celery.bin.celery import CeleryCommand as _CeleryCommand
from flask.ext.script import Command, Option, Manager

import argparse

__all__ = ['Celery', 'CeleryCommand']


class _CeleryConfig(object):

    def __init__(self, celery):
        self.celery = celery


class Celery(_Celery):

    def __init__(self, app=None, *args, **kwargs):
        super(_Celery, self).__init__(*args, **kwargs)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.conf.update(app.config)
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['celery'] = _CeleryConfig(self)

    def __reduce_args__(self):
        return super().__reduce_args__()


class _TransferCommand(Command):

    def __init__(self, celery_command):
        super(Command, self).__init__()
        self.celery_command = celery_command
        for celery_option in list(celery_command.get_options()):
            self.add_option(self._transfer_option(celery_option))

    def _transfer_option(self, opt_option):
        option_kwargs = vars(opt_option)
        # args name_or_flag
        option_args = option_kwargs.pop('_short_opts') + option_kwargs.pop('_long_opts')
        # default
        if option_kwargs['default'] == ('NO', 'DEFAULT'):
            option_kwargs['default'] = None
        # type
        type_transfer = {
            'string': str,
            'int': int,
            'choice': str,
            'float': float,
            'complex': complex,
        }
        if option_kwargs['type']:
            option_kwargs['type'] = type_transfer.get(option_kwargs['type'], option_kwargs['type'])
        # action
        if option_kwargs['action'] == 'store_true':
            for key in ['const', 'type', 'nargs', 'metavar', 'choices']:
                option_kwargs.pop(key)
        elif option_kwargs['action'] == 'store':
            option_kwargs.pop('nargs')
        if option_kwargs['action'] == 'callback':
            callback_func = option_kwargs.pop('callback')
            callback_args = option_kwargs.pop('callback_args')
            callback_kwargs = option_kwargs.pop('callback_kwargs')

            class _action_cls(argparse.Action):

                def __call__(self, parser, namespace, values, option_string=None):
                    return callback_func(*callback_args, **callback_kwargs)

            arg_kwargs['action'] = _action_cls
            arg_kwargs['nargs'] = 0

        return Option(*option_args, **option_kwargs)

    def run(self, **kwargs):
        self.celery_command.run(**kwargs)


class CeleryCommand(Manager):

    def __init__(self, celery):
        super(Manager, self).__init__(usage='Perform celery command')
        for name, command_class in _CeleryCommand.commands.items():
            command_class_instance = command_class(app=celery)
            self.add_command(name, _TransferCommand(command_class_instance))


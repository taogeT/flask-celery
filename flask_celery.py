# -*- coding: UTF-8 -*-
from celery.app import App
from celery.bin.celery import CeleryCommand as _CeleryCommand
from flask.ext.script import Command, Option, Manager

import argparse


class _CeleryConfig(object):

    def __init__(self, celery):
        self.celery = celery


class Celery(App):

    def __init__(self, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.conf.update(app.config)
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['celery'] = _CeleryConfig(self)

    def __reduce_args__(self):
        return super().__reduce_args__()


def option_optparse_to_argparse(opt_option):
    opt_option_dict = vars(opt_option)
    # args name_or_flag
    arg_args = opt_option_dict['_short_opts'] + opt_option_dict['_long_opts']
    # kwargs
    arg_kwargs = {}
    # dest
    arg_kwargs['dest'] = opt_option_dict['dest']
    # help
    arg_kwargs['help'] = opt_option_dict['help']
    # nargs
    arg_kwargs['nargs'] = opt_option_dict['nargs']
    # const
    arg_kwargs['const'] = opt_option_dict['const']
    # default
    if opt_option_dict['default'] != ('NO', 'DEFAULT'):
        arg_kwargs['default'] = opt_option_dict['default']
    # type
    type_transfer = {
        'string': str,
        'int': int,
        'choice': str,
        'float': float,
        'complex': complex,
    }
    if opt_option_dict['type']:
        arg_kwargs['type'] = type_transfer[opt_option_dict['type']]
    else:
        arg_kwargs['type'] = None
    # choices
    arg_kwargs['choices'] = opt_option_dict['choices']
    # metavar
    arg_kwargs['metavar'] = opt_option_dict['metavar']
    # action
    arg_kwargs['action'] = opt_option_dict['action']
    if arg_kwargs['action'] == 'store_true':
        for key in ['const', 'type', 'nargs', 'metavar', 'choices']:
            arg_kwargs.pop(key)
    elif arg_kwargs['action'] == 'store':
        arg_kwargs.pop('nargs')
    if arg_kwargs['action'] == 'callback':
        callback_func = opt_option_dict['callback']
        callback_args = opt_option_dict['callback_args']
        callback_kwargs = opt_option_dict['callback_kwargs']

        class _action_cls(argparse.Action):

            def __call__(self, parser, namespace, values, option_string=None):
                return callback_func(*callback_args, **callback_kwargs)

        arg_kwargs['action'] = _action_cls
        arg_kwargs['nargs'] = 0

    return Option(*arg_args, **arg_kwargs)


class TransferCommand(Command):

    def __init__(self, celery_command):
        super().__init__()
        self.celery_command = celery_command
        for celery_option in list(celery_command.get_options()):
            transfer_option = option_optparse_to_argparse(celery_option)
            self.add_option(transfer_option)

    def run(self, **kwargs):
        self.celery_command.run(**kwargs)


def CeleryCommand(app):
    command_manager = Manager(usage='Perform celery command')
    for name, command_class in _CeleryCommand.commands.items():
        command_class_instance = command_class(app=app)
        command_manager.add_command(name, TransferCommand(command_class_instance))
    return command_manager

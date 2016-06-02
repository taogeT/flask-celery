# -*- coding: utf-8 -*-
from . import celery


@celery.task
def add(x, y):
    return x + y

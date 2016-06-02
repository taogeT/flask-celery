# -*- coding: utf-8 -*-
from .. import celery


@celery.task
def minus(x, y):
    return x - y

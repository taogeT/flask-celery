# -*- coding: utf-8 -*-
from flask import request
from ..tasks import add
from . import test
from .tasks import minus


@test.route("/")
def hello_world(x=16, y=16):
    x = int(request.args.get("x", x))
    y = int(request.args.get("y", y))
    addres = add.apply_async(args=[x, y])
    minusres = minus.apply_async(args=[x, y])
    context = {"addid": addres.task_id, "minusid": minusres.task_id,
               "x": x, "y": y}
    return """Hello world: add(%(x)s, %(y)s) = <a href="/addresult/%(addid)s">%(addid)s</a>
          minus(%(x)s, %(y)s) = <a href="/minusresult/%(minusid)s">%(minusid)s</a>""" % context


@test.route("/addresult/<task_id>")
def show_add_result(task_id):
    retval = add.AsyncResult(task_id).get()
    return repr(retval)


@test.route("/minusresult/<task_id>")
def show_minus_result(task_id):
    retval = minus.AsyncResult(task_id).get()
    return repr(retval)

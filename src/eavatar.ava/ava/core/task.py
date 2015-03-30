# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import logging
import gevent
from uuid import uuid1
from gevent import Greenlet

logger = logging.getLogger(__name__)


class TaskProxy(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)


class Trigger(Greenlet):
    def __init__(self, task, args, kwargs):
        super(Trigger, self).__init__()
        self.task = task
        self.args = args
        self.kwargs = kwargs

    def call(self):
        try:
            self.value = self.task(*self.args, **self.kwargs)
        except Exception as ex:
            self._exception = ex

    def _run(self):
        raise NotImplementedError()


class OnceTrigger(Trigger):
    def __init__(self, task, seconds=0, args=None, kwargs=None):
        super(OnceTrigger, self).__init__(task, *args, **kwargs)
        self.seconds = seconds

    def _run(self):
        if self.seconds > 0:
            gevent.sleep(self.seconds)
        self.call()


class TaskEngine(object):

    def __init__(self):
        self.context = None
        self._triggers = {}
        self._tasks = {}

    def start(self, ctx):
        logger.debug("Starting task engine...")
        self.context = ctx
        self.context['task_engine'] = self

    def stop(self, ctx):
        logger.debug("Stopping task engine...")

    def run_once(self, task, delayed_secs, args, kwargs):
        """
        Schedules a one-time task.

        :param task:
        :param delayed_secs:
        :return: the task's ID.
        """
        trigger = OnceTrigger(task, delayed_secs, args, kwargs)
        task_id = uuid1().hex
        self._triggers[task_id] = trigger
        trigger.start()
        return task_id

    def run_periodic(self, task, interval, start_time=None, stop_time=None):
        """
        Schedules a periodic task.

        :param task:
        :param interval:
        :param start_time: If None, start immediately.
        :param stop_time: If None, the task run indefinitely.
        :return: the task's ID.
        """
        task_id = uuid1().hex
        raise NotImplementedError()

    def cancel(self, task_id):
        """
        Cancels the specified task.

        :param task_id:
        :return:
        """
        raise NotImplementedError()
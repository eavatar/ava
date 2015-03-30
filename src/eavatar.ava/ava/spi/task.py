# -*- coding: utf-8 -*-
"""
Task declaration
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from .context import instance as agent

task_engine = agent.task_engine


def task(func):
    """
    Marks a function as a task template(code, arguments, etc).

    :param func:
    :return:
    """
    return func


def run_once(task, seconds=0, args=None, kwargs=None):
    """
    Run a one-time task later after the specified seconds.

    :param task:
    :param seconds:
    :return:
    """
    return task_engine.run_once(seconds)


def run_periodic(task, interval, start_time=None, stop_time=None, args=None, kwargs=None):
    """

    :param task:
    :param interval: the interval in seconds.
    :param start_time: the timestamp from which the task can be run
    :param stop_time: the timestamp before which the task should be run
    :return:
    """
    return task_engine.run_periodic(task, interval, start_time, stop_time)


def run_at(task, time_points, args, kwargs):
    """ Schedules a task to run with the given time points.

    :param task:
    :param time_spec:
    :return:
    """
    raise NotImplementedError()
# -*- coding: utf-8 -*-
from django.dispatch import Signal


task_completed = Signal(providing_args=['task_id'])
task_canceled = Signal(providing_args=['task_id'])
task_assigned = Signal(providing_args=['task_id'])


__all__ = [
    'task_assigned',
    'task_canceled',
    'task_completed'
]

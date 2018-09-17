# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver

from workflows.models import Task


@receiver(post_save, sender=Task, dispatch_uid='check_if_task_has_new_assignee')
def check_if_task_has_new_assignee(sender, instance, created, *args, **kwargs):
    pass


@receiver(post_save, sender=Task, dispatch_uid='check_if_task_has_been_completed')
def check_if_task_has_been_completed(sender, instance, created, *args, **kwargs):
    pass

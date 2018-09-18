# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres import fields as postgres_fields


class WorkflowBase(models.Model):
    label = models.CharField(max_length=100)
    internal_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    snoozing = postgres_fields.ArrayField(models.PositiveIntegerField(), null=True, blank=True)

    def __repr__(self):
        return '{id}: {workflow} - {internal_name}'.format(
            id=self.pk,
            workflow=self.label,
            internal_name=self.internal_name
        )

    def is_active(self):
        return self.active

    def has_pending_tasks(self):
        from workflows.models import Task
        return self.tasks.filter(status=Task.ACTIVE_STATUS).exists()

    def is_snoozeable(self):
        return len(self.snoozing) > 0


__all__ = [
    'WorkflowBase',
]

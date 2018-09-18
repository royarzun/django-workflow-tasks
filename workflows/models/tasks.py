# -*- coding: utf-8 -*-
import arrow

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F, Q
from django.template import Template, Context


class TaskManager(models.Manager):
    def get_queryset(self):
        return super(TaskManager, self).get_queryset().prefetch_related('values')

    def active_tasks(self):
        now = arrow.utcnow().datetime
        return self.get_queryset() \
            .filter(status=Task.ACTIVE_STATUS) \
            .filter(Q(valid_until__isnull=True) | Q(valid_until__lte=now)) \
            .filter(Q(assignable_from__isnull=True) | Q(assignable_from__gte=now))

    def inactive_tasks(self):
        now = arrow.utcnow().datetime
        return self.get_queryset() \
            .exclude(status=Task.ACTIVE_STATUS) \
            .filter(Q(valid_until__isnull=True) | Q(valid_until__gt=now)) \
            .filter(Q(assignable_from__isnull=True) | Q(assignable_from__lte=now))

    def look_for_duplicated_tasks(self, task):
        return self.get_queryset() \
            .annotate(calculated_footprint=F('values__key')) \
            .filter(calculated_footprint=task.footprint)


class Task(models.Model):
    ACTIVE_STATUS = 'ACTIVE'
    ALLOWED_STATUSES = (
        ('ACTIVE', 'Active'),
        ('CANCELED', 'Canceled'),
        ('COMPLETED', 'Completed')
    )
    TERMINAL_STATUSES = ['CANCELED', 'COMPLETED']

    workflow = models.ForeignKey('workflows.WorkflowBase', related_name='tasks')
    status = models.CharField(max_length=50, choices=ALLOWED_STATUSES, default=ACTIVE_STATUS, db_index=True)
    priority = models.IntegerField(default=0)

    assignable_from = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(null=True, blank=True)

    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    assignee_id = models.PositiveIntegerField(null=True)
    assignee_object = GenericForeignKey('content_type', 'assignee_id')

    objects = TaskManager()

    def _footprint(self):
        return '-'.join([
            '{key}:{value}'.format(key=tv.key, value=tv.value)
            for tv in self.values.only('key', 'value').distinct('key').order_by('key', '-created')
        ])

    @property
    def description(self):
        """Returns description as rendered html with the workflow and task as part of the context"""
        template = Template(self.workflow.description)
        context = Context(self.get_values())
        return template.render(context)

    def get_values(self):
        """Returns task values as dict

        In case task has repeated keys it will return the latest added value

        :return: dict()
        """
        values = [(tv.key, tv.value)
                  for tv in self.values.only('key', 'value').distinct('key').order_by('key', '-created')]
        return dict(values)

    def is_active(self):
        return self.status == self.ACTIVE_STATUS

    def is_assignable(self):
        return True

    def is_completed(self):
        return self.status in self.TERMINAL_STATUSES

    def is_valid(self):
        if self.valid_until is not None:
            return self.valid_until < arrow.utcnow().datetime
        return True

    def mark_as_completed(self):
        self.status = 'COMPLETED'
        self.save(update_fields=['status'])

    def cancel(self):
        self.status = 'CANCELED'
        self.save(update_fields=['status'])


class TaskValue(models.Model):
    ALLOWED_CONTENT_TYPES = (
        ('INTEGER', 'Integer'),
        ('STRING', 'String'),
        ('DATETIME', 'Datetime')
    )

    task = models.ForeignKey('workflows.Task', related_name='values', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=50, db_index=True)
    content_type = models.CharField(choices=ALLOWED_CONTENT_TYPES, max_length=50, db_index=True)
    value = models.TextField()

    def deserialize(self):
        if self.content_type == 'INTEGER':
            return int(self.value)
        if self.content_type == 'STRING':
            return str(self.value)
        if self.content_type == 'DATETIME':
            return arrow.get(self.value).datetime

        return self.value


__all__ = [
    'Task',
    'TaskValue'
]

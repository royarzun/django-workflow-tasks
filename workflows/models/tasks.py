# -*- coding: utf-8 -*-
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template import Template, Context


class TaskManager(models.Manager):
    def get_queryset(self):
        return super(TaskManager, self).get_queryset().prefetch_related('values')

    def active_tasks(self):
        return self.get_queryset().filter(status=Task.ACTIVE_STATUS)

    def inactive_tasks(self):
        return self.get_queryset().exclude(status=Task.ACTIVE_STATUS)


class Task(models.Model):
    ACTIVE_STATUS = 'ACTIVE'
    ALLOWED_STATUSES = (
        ('ACTIVE', 'Active'),
        ('CANCELED', 'Canceled'),
        ('COMPLETED', 'Completed')
    )
    TERMINAL_STATUSES = ['CANCELED', 'COMPLETED']

    workflow = models.ForeignKey('WorkflowBase', related_name='tasks')
    status = models.CharField(max_length=50, choices=ALLOWED_STATUSES, default=ACTIVE_STATUS, db_index=True)
    priority = models.IntegerField(default=0)

    assignable_from = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(null=True, blank=True)

    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    assignee_id = models.PositiveIntegerField(null=True, max_length=10)
    assignee_object = GenericForeignKey('content_type', 'assignee_id')

    objects = TaskManager()

    @property
    def description(self):
        template = Template(self.workflow.description)
        context = Context(self.get_values())
        return template.render(context)

    def get_values(self):
        values = [(tv.key, tv.value)
                  for tv in self.values.only('key', 'value').distinct('key').order_by('key', '-created')]
        return dict(values)

    def is_active(self):
        return self.status == self.ACTIVE_STATUS

    def is_assignable(self):
        return True

    def is_completed(self):
        return self.status in self.TERMINAL_STATUSES

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

    task = models.ForeignKey('Task', related_name='values', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=50, db_index=True)
    value_content_type = models.CharField(choices=ALLOWED_CONTENT_TYPES, max_length=50, db_index=True)
    value = models.TextField()


__all__ = [
    'Task',
    'TaskValue'
]

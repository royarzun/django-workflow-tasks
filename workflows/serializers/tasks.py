# -*- coding: utf-8 -*-
from rest_framework import serializers
from workflows.models import Task, TaskValue


class TaskValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskValue


class TaskSerializer(serializers.ModelSerializer):
    values = TaskValueSerializer(many=True, allow_null=True)

    class Meta:
        model = Task


__all__ = ['TaskSerializer']

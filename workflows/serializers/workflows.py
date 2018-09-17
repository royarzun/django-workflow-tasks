# -*- coding: utf-8 -*-
from rest_framework import serializers
from workflows.models import WorkflowBase


class WorkflowSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkflowBase


__all__ = ['WorkflowSerializer']

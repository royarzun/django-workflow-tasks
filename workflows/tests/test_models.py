# -*- coding: utf-8 -*-
from django.test import TestCase
from workflows.models import Task, WorkflowBase
from workflows.mixins import NonRepeatable


class ModelsMixinTestCase(TestCase):

    def test_assert_we_can_create_a_non_repeatable_task(self):
        class NonRepeatableTask(Task, NonRepeatable):
            pass
        workflow = WorkflowBase.objects.create(label="foo", internal_name="internal_foo", snoozing=[])

        task_1 = NonRepeatableTask.objects.create(workflow=workflow)
        task_1.values.create(key="k1", value="value1")
        task_1.values.create(key="k2", value="value2")
        task_1.values.create(key="k3", value="value3")

        task_2 = NonRepeatableTask.objects.create(workflow=workflow)
        task_2.values.create(key="k1", value="value1")
        task_2.values.create(key="k2", value="value2")
        task_2.values.create(key="k3", value="value3")

        self.assertTrue(task_1 == task_2)

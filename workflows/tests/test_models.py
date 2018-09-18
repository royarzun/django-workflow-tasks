# -*- coding: utf-8 -*-
import arrow
from datetime import datetime
from django.test import TestCase
from model_mommy import mommy


class ModelsMixinTestCase(TestCase):

    def test_assert_we_can_create_a_non_repeatable_task(self):
        pass


class TaskValueModelTestCase(TestCase):
    wf = None
    task = None

    def setUp(self):
        self.wf = mommy.make('workflows.WorkflowBase')
        self.task = mommy.make('workflows.Task', workflow=self.wf)

    def test_model_footprint(self):
        now = arrow.utcnow().datetime
        self.task.values.create(key="k1", value="v1", content_type="STRING")
        self.task.values.create(key="k2", value=str(now), content_type="DATETIME")

        self.assertEqual("k1:v1-k2:{serialized_value}".format(serialized_value=str(now)), self.task._footprint())

    def test_deserialize_content(self):
        now = arrow.utcnow().datetime
        str_value = self.task.values.create(key="k1", value="v1", content_type="STRING")
        dt_value = self.task.values.create(key="k2", value=str(now), content_type="DATETIME")
        int_value = self.task.values.create(key="k2", value=str(1), content_type="INTEGER")
        self.assertIsInstance(str_value.deserialize(), str)
        self.assertIsInstance(dt_value.deserialize(), datetime)
        self.assertIsInstance(int_value.deserialize(), int)

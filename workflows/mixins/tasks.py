# -*- coding: utf-8 -*-
import arrow

from django.apps import apps as django_apps

TaskBaseModel = django_apps.get_model('workflows', 'Task')


class Expirable(object):

    def is_valid(self):
        valid_until = getattr(self, 'valid_until')
        if valid_until is not None:
            return arrow.utcnow().datetime < valid_until
        else:
            return True


class NonRepeatable(object):

    def __eq__(self, other):
        """Given that the tasks to compare belong to the same workflow, we will compare
        based on the common task value keys the tasks might have declared
        """
        self_values_callable = getattr(self, 'get_values')
        self_values = self_values_callable()
        other_values = other.get_values()
        distinct_values = 0

        if not len(self_values()) or not len(other_values):
            return False

        for key in set(self_values) & set(other_values):
            if self_values[key] != other_values[key]:
                distinct_values += 1

        return (
            isinstance(other, TaskBaseModel) and
            not distinct_values and
            getattr(self, 'workflow_id') == other.workflow_id
        )

    def __hash__(self):
        values = getattr(self, 'values')
        key_values = ("{key}-{value}".format(key=tv.key, value=tv.value) for tv in values.all())
        return hash((getattr(self, 'workflow_id'), key_values))


class AssignableLater(object):

    def is_assignable(self):
        assignable_from = getattr(self, 'assignable_from')
        if assignable_from is not None:
            return arrow.utcnow().datetime < assignable_from
        else:
            return True


__all__ = [
    'AssignableLater',
    'Expirable',
    'NonRepeatable'
]
# -*- coding: utf-8 -*-
from workflow_tasks.settings.default import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travis_ci_test',
        'USER': 'postgres',
        'PORT': 5432,
    }
}
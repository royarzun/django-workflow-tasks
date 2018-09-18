# -*- coding: utf-8 -*-
from .default import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travis_ci_test',
        'HOST': 'localhost',
        'USER': 'postgres',
        'PORT': 5432,
    }
}

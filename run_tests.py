"""
A bootstrap script that allows for easily testing this app outside of a full 
Django project.

Base on a script published by Lukasz Dziedzia at: 
http://stackoverflow.com/questions/3841725/how-to-launch-tests-for-django-reusable-app
"""
import os
import sys
import django
from django.conf import settings

DIRNAME = os.path.dirname(__file__)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'yamlfield',
)

if django.VERSION[0] == 1 and django.VERSION[1] >= 2:
    # For versions 1.2 and up
    settings.configure(
        DEBUG = True,
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(DIRNAME, 'database.db'),
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        },
        INSTALLED_APPS = INSTALLED_APPS
    )

    from django.test.simple import DjangoTestSuiteRunner
    failures = DjangoTestSuiteRunner().run_tests(['yamlfield',], verbosity=1)
    if failures:
        sys.exit(failures)
else:
    # For earlier versions
    settings.configure(DEBUG = True,
       DATABASE_ENGINE = 'sqlite3',
       DATABASE_NAME = os.path.join(DIRNAME, 'database.db'),
       INSTALLED_APPS = INSTALLED_APPS
    )
    from django.test.simple import run_tests
    failures = run_tests(['yamlfield',], verbosity=1)
    if failures:
        sys.exit(failures)




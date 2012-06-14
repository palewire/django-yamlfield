import os
import sys
import argparse
from django.conf import settings


class QikDjangoTest(object):
    """
    A quick way to run the Django test suite without a fully-configured project.
    
    Example usage:
    
        >>> QikDjangoTest('app1', 'app2')
    
    Based on a script published by Lukasz Dziedzia at: 
    http://stackoverflow.com/questions/3841725/how-to-launch-tests-for-django-reusable-app
    """
    DIRNAME = os.path.dirname(__file__)
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'yamlfield',
    )
    
    def __init__(self, *args, **kwargs):
        self.apps = args
        self.version = self.get_test_version()
        if self.version == 'new':
            self._new_tests()
        else:
            self._old_tests()
    
    def get_test_version(self):
        from django import VERSION
        if VERSION[0] == 1 and VERSION[1] >= 2:
            return 'new'
        else:
            return 'old'
    
    def _old_tests(self):
        settings.configure(DEBUG = True,
           DATABASE_ENGINE = 'sqlite3',
           DATABASE_NAME = os.path.join(self.DIRNAME, 'database.db'),
           INSTALLED_APPS = self.INSTALLED_APPS
        )
        from django.test.simple import run_tests
        failures = run_tests(self.apps, verbosity=1)
        if failures:
            sys.exit(failures)
    
    def _new_tests(self):
        settings.configure(
            DEBUG = True,
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(self.DIRNAME, 'database.db'),
                    'USER': '',
                    'PASSWORD': '',
                    'HOST': '',
                    'PORT': '',
                }
            },
            INSTALLED_APPS = self.INSTALLED_APPS
        )
        from django.test.simple import DjangoTestSuiteRunner
        failures = DjangoTestSuiteRunner().run_tests(self.apps, verbosity=1)
        if failures:
            sys.exit(failures)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage="[args]",
        description="Run Django tests on the provided applications."
    )
    parser.add_argument('apps', nargs='+', type=str)
    args = parser.parse_args()
    QikDjangoTest(*args.apps)

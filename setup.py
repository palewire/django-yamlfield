#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from distutils.core import Command


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings
        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3'
                }
            },
            MIDDLEWARE_CLASSES=(),
            INSTALLED_APPS=('yamlfield',)
        )
        from django.core.management import call_command
        import django
        if django.VERSION[:2] >= (1, 7):
            django.setup()
        call_command('test', 'yamlfield')


setup(
    name='django-yamlfield',
    version='1.0.0',
    description='A Django database field for storing YAML data',
    author='Ben Welsh',
    author_email='ben.welsh@latimes.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=(
        'PyYAML>=3.10',
        'six>=1.4.1'
    ),
    cmdclass={'test': TestCommand,}
)

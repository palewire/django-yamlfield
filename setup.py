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
        django.setup()
        call_command('test', 'yamlfield')


setup(
    name='django-yamlfield',
    version='1.0.3',
    description='A Django database field for storing YAML data',
    author='The Los Angeles Times Data Desk',
    author_email='datadesk@latimes.com',
    url="http://django-yamlfield.readthedocs.io/",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    install_requires=(
        'PyYAML>=3.10',
        'six>=1.4.1'
    ),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'License :: OSI Approved :: MIT License',
    ],
    cmdclass={'test': TestCommand,}
)

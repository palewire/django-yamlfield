<meta http-equiv="Refresh" content="0; url='https://palewi.re/docs/django-yamlfield/'" />

django-yamlfield
================

A Django database field for storing [YAML](http://en.wikipedia.org/wiki/YAML) data

Getting started
---------------

Install this module

```bash
pipenv install django-yamlfield
```

Add it to one of your models.

```python
from django.db import models
from yamlfield.fields import YAMLField

class YourModel(models.Model):
    yaml = YAMLField()
```

That's it! You can now start storing YAML data.

Credits
-------

This module was developed by Ben Welsh, based on Brad Jasper's [django-jsonfield](https://github.com/bradjasper/django-jsonfield).

Other resources
---------------

[![Build Status](https://travis-ci.org/datadesk/django-yamlfield.png?branch=master)](https://travis-ci.org/datadesk/django-yamlfield)
[![PyPI version](https://badge.fury.io/py/django-yamlfield.png)](http://badge.fury.io/py/django-yamlfield)
[![Coverage Status](https://coveralls.io/repos/datadesk/django-yamlfield/badge.png?branch=master)](https://coveralls.io/r/datadesk/django-yamlfield?branch=master)

* Repo: [https://github.com/datadesk/django-yamlfield](https://github.com/datadesk/django-yamlfield)
* Issues: [https://github.com/datadesk/django-yamlfield/issues](https://github.com/datadesk/django-yamlfield/issues)
* Packaging: [https://pypi.python.org/pypi/django-yamlfield](https://pypi.python.org/pypi/django-yamlfield)
* Testing: [https://travis-ci.org/datadesk/django-yamlfield](https://travis-ci.org/datadesk/django-yamlfield)
* Coverage: [https://coveralls.io/r/datadesk/django-yamlfield](https://coveralls.io/r/datadesk/django-yamlfield)

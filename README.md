<pre><code>Yb  dP    db    8b    d8 88     888888 88 888888 88     8888b.  
 YbdP    dPYb   88b  d88 88     88__   88 88__   88      8I  Yb 
  8P    dP__Yb  88YbdP88 88  .o 88""   88 88""   88  .o  8I  dY 
 dP    dP""""Yb 88 YY 88 88ood8 88     88 888888 88ood8 8888Y"  </code></pre>

A Django database field for storing "YAML":http://en.wikipedia.org/wiki/YAML data

[![Build Status](https://travis-ci.org/datadesk/django-yamlfield.png?branch=master)](https://travis-ci.org/datadesk/django-yamlfield)
[![PyPI version](https://badge.fury.io/py/django-yamlfield.png)](http://badge.fury.io/py/django-yamlfield)
[![Coverage Status](https://coveralls.io/repos/datadesk/django-yamlfield/badge.png?branch=master)](https://coveralls.io/r/datadesk/django-yamlfield?branch=master)

* Issues: [https://github.com/datadesk/django-yamlfield/issues](https://github.com/datadesk/django-yamlfield/issues)
* Packaging: [https://pypi.python.org/pypi/django-yamlfield](https://pypi.python.org/pypi/django-yamlfield)
* Testing: [https://travis-ci.org/datadesk/django-yamlfield](https://travis-ci.org/datadesk/django-yamlfield)
* Coverage: [https://coveralls.io/r/datadesk/django-yamlfield](https://coveralls.io/r/datadesk/django-yamlfield)

Getting started
---------------

Install this module

```bash
$ pip install django-yamlfield
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

This module was developed by Ben Welsh, based on Brad Jasper's "django-jsonfield":https://github.com/bradjasper/django-jsonfield.

The rest
--------

* Supports Django version 1.2 and up and Python versions 2.5, 2.6, 2.7, 3.2 and 3.3 which are routinely tested using "Travis CI":http://travis-ci.org/#!/datadesk/django-yamlfield

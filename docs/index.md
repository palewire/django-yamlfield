```{include} _templates/nav.html
```

# django-yamlfield

A Django database field for storing [YAML](http://en.wikipedia.org/wiki/YAML) data

## Getting started

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

## Links

* Repo: [https://github.com/datadesk/django-yamlfield](https://github.com/datadesk/django-yamlfield)
* Issues: [https://github.com/datadesk/django-yamlfield/issues](https://github.com/datadesk/django-yamlfield/issues)
* Packaging: [https://pypi.python.org/pypi/django-yamlfield](https://pypi.python.org/pypi/django-yamlfield)

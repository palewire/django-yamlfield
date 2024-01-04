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
    data = YAMLField()
```

That's it! You can now start storing Python objects as YAML.

```python
obj = YourModel.objects.create(
    data={"a": "foo", "b": "baz"}
)
obj.save()
```

### Other resources

* Issues: [github.com/palewire/django-yamlfield/issues](https://github.com/palewire/django-yamlfield/issues)
* Packaging: [pypi.python.org/pypi/django-yamlfield](https://pypi.python.org/pypi/django-yamlfield)
* Testing: [github.com/palewire/django-yamlfield/actions](https://github.com/palewire/django-yamlfield/actions)
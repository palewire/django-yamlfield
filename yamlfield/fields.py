import six
import yaml
import collections
from django.db import models
from django import forms
from django.utils.encoding import python_2_unicode_compatible
from .serializers import OrderedDumper, OrderedLoader


def yaml_to_python(yaml_text):
    """
    converts yaml(Text) to OrderedDict python obj
    """
    if yaml_text in ("", None):
        return None

    if isinstance(yaml_text, six.string_types):
        try:
            return yaml.load(yaml_text, OrderedLoader)
        except ValueError:
            pass

    # converted already
    if isinstance(yaml_text, (collections.Mapping, collections.Iterable)):
        return yaml_text

    return yaml_text


def yaml_to_db(python_obj):
    """
    converts yaml(OrderedDict) to Text database obj
    """
    if python_obj in (None, ""):
        return ""

    # converted already
    if isinstance(python_obj, six.string_types):
        return python_obj

    if isinstance(python_obj, (collections.Mapping, collections.Iterable)):
        return yaml.dump(python_obj,
                         Dumper=OrderedDumper,
                         default_flow_style=False)

    return python_obj


@python_2_unicode_compatible
class YAMLField(models.Field):
    """
    YAMLField is a TextField that serializes and deserializes YAML data
    from the database.

    Based on https://github.com/bradjasper/django-jsonfield
    """
    description = "A django yaml field"

    def get_internal_type(self):
        return 'TextField'

    def from_db_value(self, value, expression, connection, context):
        """
        Called in all circumstances when the data is loaded from the database
        """
        return yaml_to_python(value)

    def to_python(self, value):
        """
        Called by deserialization and during the clean() method used from forms
        """
        return yaml_to_python(value)

    def get_db_prep_save(self, value, connection):
        """
        Convert our Python object to a string of YAML before we save.
        """
        return super(YAMLField, self).get_db_prep_save(
            yaml_to_db(value),
            connection=connection
        )

    def value_from_object(self, obj):
        """
        Returns the value of this field in the given model instance.

        We need to override this so that the YAML comes out properly formatted
        in the admin widget.
        """
        value = getattr(obj, self.attname)
        return yaml_to_db(value)

    def formfield(self, **kwargs):
        defaults = {'widget': forms.Textarea}
        defaults.update(kwargs)
        return super(YAMLField, self).formfield(**defaults)

    def __str__(self):
        return 'YamlField'

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^yamlfield\.fields\.YAMLField"])
except ImportError:
    pass

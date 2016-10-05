import six
import yaml
from django.core.exceptions import ValidationError
from django.db import models
from .serializers import OrderedDumper, OrderedLoader


class YAMLField(models.TextField):
    """
    YAMLField is a TextField that serializes and deserializes YAML data
    from the database.

    Based on https://github.com/bradjasper/django-jsonfield
    """
    def db_type(self, connection):
        return 'TextField'

    def to_python(self, value):
        """
        Convert our YAML string to a Python object
        after we load it from the DB.
        """
        if value == "":
            return None
        try:
            if isinstance(value, six.string_types):
                return yaml.load(value, OrderedLoader)
        except ValueError:
            raise ValidationError("Enter valid YAML")
        return value

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def get_prep_value(self, value):
        """
        Convert our Python object to a string of YAML before we save.
        """
        if not value or value == "":
            return ""
        if isinstance(value, (dict, list)):
            value = yaml.dump(
                value,
                Dumper=OrderedDumper,
                default_flow_style=False
            )
        return value

    def value_from_object(self, obj):
        """
        Returns the value of this field in the given model instance.

        We need to override this so that the YAML comes out properly formatted
        in the admin widget.
        """
        value = getattr(obj, self.attname)
        if not value or value == "":
            return value
        return yaml.dump(
            value,
            Dumper=OrderedDumper,
            default_flow_style=False
        )


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^yamlfield\.fields\.YAMLField"])
except ImportError:
    pass

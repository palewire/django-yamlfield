import yaml
from django.db import models
from django.core.exceptions import ValidationError
from .serializers import OrderedDumper, OrderedLoader


class YAMLField(models.TextField):

    def from_db_value(self, value, expression, connection, context=None):
        return self.to_python(value)

    def to_python(self, value):
        """
        Convert our YAML string to a Python object
        after we load it from the DB.
        """
        if value == "":
            return None
        try:
            if isinstance(value, str):
                return yaml.load(value, OrderedLoader)
        except ValueError:
            raise ValidationError("Enter valid YAML")
        return value

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

import yaml

from django.core.exceptions import ValidationError
from django.db import models

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

        if isinstance(value, str):
            try:
                return yaml.load(value, OrderedLoader)
            except yaml.composer.ComposerError:
                # try to read multiple yaml file separated with ---
                try:
                    return list(yaml.load_all(value, yaml.FullLoader))
                except ValueError:
                    raise ValidationError("Enter valid YAML")
            except ValueError:
                raise ValidationError("Enter valid YAML")
        return value

    def get_prep_value(self, value):
        """
        Convert our Python object to a string of YAML before we save.
        """
        if not value or value == "":
            return ""
        if isinstance(value, dict):
            value = yaml.dump(value, Dumper=OrderedDumper, default_flow_style=False)
        elif isinstance(value, list):
            dumped = ''
            for count, d in enumerate(value, start=1):
                dumped += yaml.dump(d, Dumper=OrderedDumper, default_flow_style=False)
                if len(value) > count:
                    dumped += "---\n"
            return dumped
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
        if isinstance(value, list):
            # multiple yaml file seperated with ---
            dumped = ''
            for count, d in enumerate(value, start=1):
                dumped += yaml.dump(d, Dumper=OrderedDumper, default_flow_style=False)
                if len(value) > count:
                    dumped += "---\n"
            return dumped
        else:
            return yaml.dump(value, Dumper=OrderedDumper, default_flow_style=False)

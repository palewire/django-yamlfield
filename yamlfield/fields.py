import yaml
from django.db import models
from django.core.serializers.pyyaml import DjangoSafeDumper


class YAMLField(models.TextField):
    """
    YAMLField is a TextField that serializes and deserializes YAML data
    from the database.

    Based on https://github.com/bradjasper/django-jsonfield
    """
    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """
        Convert our YAML string to a Python object after we load it from the DB.
        """
        if value == "":
            return None
        try:
            if isinstance(value, basestring):
                return yaml.load(value)
        except ValueError:
            pass
        return value

    def get_db_prep_save(self, value, connection, prepared=False):
        """
        Convert our Python object to a string of YAML before we save.
        """
        if not value or value == "":
            return ""
        if isinstance(value, (dict, list)):
            value = yaml.dump(value, Dumper=DjangoSafeDumper,
                default_flow_style=False)
        return super(YAMLField, self).get_db_prep_save(value, connection)

    def value_from_object(self, obj):
        """
        Returns the value of this field in the given model instance.

        We need to override this so that the YAML comes out properly formatted
        in the admin widget.
        """
        value = getattr(obj, self.attname)
        if not value or value == "":
            return value
        return yaml.dump(value, Dumper=DjangoSafeDumper,
            default_flow_style=False)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^yamlfield\.fields\.YAMLField"])
except ImportError:
    pass


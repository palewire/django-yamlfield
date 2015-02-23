from collections import OrderedDict
import six
import yaml
from django.db import models
from django.core.serializers.pyyaml import DjangoSafeDumper


def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    """
    From http://stackoverflow.com/a/21912744/284164
    # usage example:
    ordered_load(stream, yaml.SafeLoader)
    """
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    """
    From http://stackoverflow.com/a/21912744/284164
    # usage example:
    ordered_dump(data, Dumper=yaml.SafeDumper)
    """
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


class YAMLField(six.with_metaclass(models.SubfieldBase, models.TextField)):
    """
    YAMLField is a TextField that serializes and deserializes YAML data
    from the database.

    Based on https://github.com/bradjasper/django-jsonfield
    """
    def to_python(self, value):
        """
        Convert our YAML string to a Python object
        after we load it from the DB.
        """
        if value == "":
            return None
        try:
            if isinstance(value, six.string_types):
                return ordered_load(value, yaml.SafeLoader)
        except ValueError:
            pass
        return value

    def get_db_prep_save(self, value, connection):
        """
        Convert our Python object to a string of YAML before we save.
        """
        if not value or value == "":
            return ""
        if isinstance(value, (dict, list)):
            value = ordered_dump(
                value,
                Dumper=DjangoSafeDumper,
                default_flow_style=False
            )

        return super(YAMLField, self).get_db_prep_save(
            value,
            connection=connection
        )

    def value_from_object(self, obj):
        """
        Returns the value of this field in the given model instance.

        We need to override this so that the YAML comes out properly formatted
        in the admin widget.
        """
        value = getattr(obj, self.attname)
        if not value or value == "":
            return value
        return ordered_dump(
            value,
            Dumper=DjangoSafeDumper,
            default_flow_style=False
        )

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^yamlfield\.fields\.YAMLField"])
except ImportError:
    pass

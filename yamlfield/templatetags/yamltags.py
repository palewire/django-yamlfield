from django import template
import yaml
from yamlfield.serializers import OrderedDumper

register = template.Library()

@register.filter
def as_text(value):
    """convert python representation to text for display"""

    if not value or value == "":
        return ""
    if isinstance(value, (dict, list)):
        value = yaml.dump(
            value,
            Dumper=OrderedDumper,
            default_flow_style=False
        )
    return value
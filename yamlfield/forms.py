# -*- coding:utf-8 -*-

import yaml

from django.core.serializers.pyyaml import DjangoSafeDumper
from django.forms import fields, util
from django.utils.translation import ugettext as _

class YAMLFormField(fields.Field):
    """
    YAML Form field
    """
    default_error_messages = {
        'invalid': _(u'Invalid YAML format'), }

    def clean(self, value):
        """
        Validates the given value. Raises ValidationError for any errors.
        :param value: string
        :return: string
        """
        value = super(YAMLFormField, self).clean(value)

        # allow an empty value on an optional field
        if value is None:
            return value

        # check of value
        try:
           value = yaml.load(value)
        except (yaml.scanner.ScannerError, yaml.parser.ParserError), e:
            try:
                message = util.ValidationError(u'%s: %s' % (
                    self.default_error_messages.get('invalid', ''),
                    unicode(e)))
            except:
                message = self.default_error_messages.get('invalid', '')
            raise util.ValidationError(message)
        val = yaml.dump(
            value,
            Dumper=DjangoSafeDumper,
            allow_unicode=True,
            default_flow_style=True, )
        try:
            val.index('...')
            raise util.ValidationError(
                self.default_error_messages.get('invalid', ''))
        except ValueError:
            pass
        return value

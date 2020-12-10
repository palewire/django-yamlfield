"""
Conf for :mod:`yamlfield` application

"""
from appconf import AppConf


class YAMLFieldAppConf(AppConf):
    DUMPER_ALLOW_UNICODE = True
    DUMPER_DEFAULT_FLOW_STYLE = False

    class Meta:
        prefix = "yamlfield"

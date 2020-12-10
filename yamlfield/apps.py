from django.apps import AppConfig


class YAMLFieldAppConfig(AppConfig):
    name = "yamlfield"
    verbose_name = "YAML field"

    def ready(self) -> None:
        super().ready()
        from yamlfield.conf import YAMLFieldAppConf  # noqa

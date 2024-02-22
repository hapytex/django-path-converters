from django.apps import AppConfig


class PathConvertersConfig(AppConfig):
    name = 'django_path_converters'
    verbose_name = 'Django path converters'

    def ready(self):
        import django_path_converters.converters  # noqa

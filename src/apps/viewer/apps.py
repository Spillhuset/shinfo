from django.apps import AppConfig


class ViewerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.viewer'

    def ready(self):
        import apps.viewer.signals

from django.apps import AppConfig


class ScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.schedules'
    verbose_name = 'Tidsperioder for innholdsvisning'

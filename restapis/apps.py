from django.apps import AppConfig


class RestapisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restapis'
    def ready(self):
        import restapis.signals

from django.apps import AppConfig


class LittlelemonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'littleLemon'

    def ready(self):
        import littleLemon.signals

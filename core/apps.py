from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        import core.signals  # Importez les signaux ici

from django.apps import AppConfig



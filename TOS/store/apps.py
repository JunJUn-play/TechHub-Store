# store/apps.py
from django.apps import AppConfig

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TOS.store'

    def ready(self):
        import TOS.store.signals  # This 'wires' the triggers
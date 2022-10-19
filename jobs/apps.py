from django.apps import AppConfig
import os


class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'

    def ready(self):
        super().ready()
        from . import updater
        if os.environ.get('RUN_MAIN', None) != 'true':
            updater.start()

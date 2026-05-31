from django.apps import AppConfig


class TailappConfig(AppConfig):
    name = 'tailapp'

    default_auto_field='django.db.models.BigAutoField'

    def ready(self):

        import tailapp.signals

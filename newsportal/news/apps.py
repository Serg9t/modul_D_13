from django.apps import AppConfig


class NewsConfig(AppConfig):
    verbose_name = 'Новостной портал'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        from . import signals

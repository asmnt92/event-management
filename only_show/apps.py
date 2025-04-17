from django.apps import AppConfig


class OnlyShowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'only_show'

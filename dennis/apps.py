from django.apps import AppConfig


class DennisConfig(AppConfig):
    name = 'dennis'

    # for signals

    def ready(self):
        import dennis.signals

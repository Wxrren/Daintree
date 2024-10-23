from django.apps import AppConfig
# flake8: noqa


class CheckoutConfig(AppConfig):
    name = 'checkout'

    def ready(self):
        import checkout.signals

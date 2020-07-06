from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RegisterConfig(AppConfig):
    name = "cdsso.contrib.register"
    verbose_name = _("Register")

    def ready(self):
        try:
            import cdsso.contrib.register.signals  # noqa F401
        except ImportError:
            pass

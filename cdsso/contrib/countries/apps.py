from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CountriesConfig(AppConfig):
    name = "cdsso.contrib.countries"
    verbose_name = _("Countries")

    def ready(self):
        try:
            import cdsso.contrib.countries.signals  # noqa F401
        except ImportError:
            pass

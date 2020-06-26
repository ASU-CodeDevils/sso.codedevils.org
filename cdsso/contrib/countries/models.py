from django.db import models
from django.utils.translation import ugettext_lazy as _

class Country(models.Model):
    """
    Defines a country and its locale information. All country information is pulled from
    the restcountries.eu API and is periodically updated. See more info at https://restcountries.eu/
    """
    name = models.CharField(db_column="Name", max_length=80, blank=False, null=False, verbose_name=_("Name"))
    native_name = models.CharField(db_column="NativeName", max_length=80, blank=False, null=False,
                                   verbose_name=_("Native Name"))
    alpha2_code = models.CharField(db_column="Alpha2Code", max_length=2, blank=True, null=True,
                                   verbose_name=_("Alpha2 Code"))
    alpha3_code = models.CharField(db_column="Alpha3Code", max_length=3, blank=True, null=True,
                                   verbose_name=_("Alpha3 Code"))
    numeric_code = models.PositiveSmallIntegerField(db_column="NumericCode", blank=True, null=True, 
                                                    verbose_name=_("Numeric code"))
    flag = models.URLField(db_column="Flag", blank=True, null=True, verbose_name=_("Flag"))

    def get_numeric_code(self):
        """Returns the 3-digit numeric code."""
        numeric_str = str(self.numeric_code)
        return numeric_str.zfill(3)

    def get_numeric_code_display(self):
        """Returns the 3-digit numeric code."""
        return self.get_numeric_code()

    class Meta:
        ordering = ["name"]
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

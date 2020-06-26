from django.contrib import admin

from cdsso.contrib.countries.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "alpha3_code"]
    search_fields = ["name", "alpha2_code", "alpha3_code", "numeric_code"]

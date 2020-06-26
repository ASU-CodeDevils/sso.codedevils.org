import logging

from cdsso.contrib.countries.models import Country
from cdsso.contrib.countries.util import get_all_countries
from config import celery_app


@celery_app.task()
def update_countries():
    """Updates countries from restcountries.eu."""

    log = logging.getLogger()
    try:
        countries = get_all_countries()
        for index in range(0, len(countries)):
            require_save = False
            country = countries[index]
            obj, created = Country.objects.get_or_create(name=country["name"])

            # this block is a klunky way of updating the country
            # it ensures that if this is a new country, the entire is updated
            # and will only update fields that have since been modified
            # logic is used over simply overwriting since database transactions are
            # more expensive than logical statements.
            if created or obj.alpha2_code != country["alpha2Code"]:
                obj.alpha2_code = country["alpha2Code"]
                require_save = True
            if created or obj.alpha3_code != country["alpha3Code"]:
                obj.alpha3_code = country["alpha3Code"]
                require_save = True
            if created or obj.native_name != country["nativeName"]:
                obj.native_name = country["nativeName"]
                require_save = True
            if created or obj.numeric_code != country["numericCode"]:
                obj.numeric_code = country["numericCode"]
                require_save = True
            if created or obj.flag != country["flag"]:
                obj.flag = country["flag"]
                require_save = True

            # saves only if the save is required
            if require_save:
                log.info(f"Country updated: {obj.name}")
                obj.save()

    # exception thrown if error with the get request
    except Exception as e:
        log.error(f"An error occurred updating countries: {str(e)}")

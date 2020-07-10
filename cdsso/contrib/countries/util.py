"""General utility to grab information from restcountries."""
import logging

import requests

log = logging.getLogger("")
BASE_URL = "https://restcountries.eu/rest/v2/"


def get_all_countries():
    """Returns all countries"""
    url = BASE_URL + "all"
    return _get(url=url)


def get_country(name: str, full_name: bool = True):
    """
    Returns a country by its name. An exception is thrown if no data is returned.

        :param name: The name of the country.
        :param full_name: Flag to determine if the full name of the country is returned, default is True.
    """
    url = BASE_URL + "name/" + name
    params = {"fullText": "true"} if full_name else None
    return _get(url=url, params=params)


def _get(url: str, params: dict = None, headers: dict = None):
    """Sends a get request."""
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        if not response.text:
            raise Exception(f"No data was returned with GET request: {url}")
        return response.json()
    else:
        raise Exception(f"{response.status_code}-level response returned from url: {url}")

import logging

from django.conf import settings
from django.http import HttpRequest
from django.utils import translation


class LanguageIdenitifcationMiddleware:
    """
    Identifies the language from the previous page and changes to that language if available on this site.
    If the user is coming from the CodeDevils website, it uses i18n URL pattern to grab the language code from the
    URL. This currently only works for the CodeDevils website.
    """
    def __init__(self, get_response: HttpRequest):
        self.get_response = get_response
        self.logger = logging.getLogger()

    def __call__(self, request):
        response = self.get_response(request)
        referer = request.META.get("HTTP_REFERER", None)
        if referer:
            cd_website = settings.CODEDEVILS_WEBSITE["BASE_URL"]

            # if the CD website, use the i18n pattern
            if referer.startswith(cd_website):
                split_url = referer.rsplit("/", 1)
                if len(split_url) > 1:
                    base_with_i18n = split_url[0].replace("http://", "").replace("https://", "")
                    print(base_with_i18n)
                    i18n_lang = base_with_i18n.split("/")[1]
                    print(i18n_lang)
                    lang = [item for item in settings.LANGUAGES if item[0] == i18n_lang]
                    if lang:
                        lang = lang[0][0]
                        # only change if we are not using the language already
                        if lang != translation.get_language():
                            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
                            translation.activate(lang)
            # TODO can use this, but need to check the current site to make sure it is not coming form
            # this site
            # else:
            #     accepted_langs = request.META.get("HTTP_ACCEPT_LANGUAGE", None)
            #     if accepted_langs:
            #         main_lang = accepted_langs.split(",", 1)[0]
            #         if main_lang != translation.get_language():
            #             response.set_cookie(settings.LANGUAGE_COOKIE_NAME, main_lang)
            #             translation.activate(main_lang)
        return response

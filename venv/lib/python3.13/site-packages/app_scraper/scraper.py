try:
    from urllib import quote_plus
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin, quote_plus

import requests
from bs4 import BeautifulSoup

from app_scraper import settings as s
from app_scraper.constants import HL_LANGUAGE_CODES, GL_COUNTRY_CODES

from app_scraper.utils import (
    build_url,
    parse_app_details,
    send_request,
)

class AppScraper(object):
    def __init__(self, hl="en", gl="us", website="apkmonk"):
        self.language = hl
        if self.language not in HL_LANGUAGE_CODES:
            raise ValueError(
                "{hl} is not a valid language interface code.".format(hl=self.language)
            )
        self.geolocation = gl
        if self.geolocation not in GL_COUNTRY_CODES:
            raise ValueError(
                "{gl} is not a valid geolocation country code.".format(
                    gl=self.geolocation
                )
            )
        self.params = {"hl": self.language, "gl": self.geolocation}

        self.website = website

    def details(self, app_id):
        """Sends a GET request and parses an application's details.
        :param app_id: the app to retrieve details, e.g. 'com.nintendo.zaaa'
        :return: a dictionary of app details
        """
        url = build_url("details", app_id, self.website)

        try:
            response = send_request("GET", url, params=self.params)
            print(url,response)
            soup = BeautifulSoup(response.content, "lxml", from_encoding="utf8")
        except requests.exceptions.HTTPError as e:
            raise ValueError(
                "Invalid application ID: {app}. {error}".format(app=app_id, error=e)
            )

        app_json = parse_app_details(soup, self.website)
        app_json.update({"app_id": app_id, "url": url})
        return app_json
import logging

try:
    from urllib import quote_plus
    from urlparse import urljoin, urlparse, parse_qs
except ImportError:
    from urllib.parse import quote_plus, urljoin, urlparse, parse_qs

import requests

from app_scraper import settings as s

log = logging.getLogger(__name__)


def default_headers():
    return {
        "Origin": "https://www.google.com",
        "User-Agent": s.USER_AGENT,
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    }

def build_url(method, id_string, website="apkmonk"):
    """Creates the absolute url for a type of object. E.g. details, developer,
    or similar.
    :param method: the corresponding method to get for an id.
    :param id_string: an id string query parameter.
    :return: a URL string.
    """
    if website == "apkmonk":
        website = s.APKMONK_URL
    elif website == "apkpure":
        website = s.APKPURE_URL
    elif website == "xpose repo":
        website = s.XPOSE_REPO_URL
    url = "{base}/{id}".format(base=website, id=id_string)
    return url


def send_request(
    method,
    url,
    data=None,
    params=None,
    headers=None,
    timeout=30,
    verify=True,
    allow_redirects=True,
):
    """Sends a request to the url and returns the response.
    :param method: HTTP method to use.
    :param url: URL to send.
    :param data: Dictionary of post data to send.
    :param headers: Dictionary of headers to include.
    :param timeout: number of seconds before timing out the request
    :param verify: a bool for requesting SSL verification.
    :return: a Response object.
    """
    data = {} if data is None else data
    params = {} if params is None else params
    headers = default_headers() if headers is None else headers

    try:
        response = requests.request(
            method=method,
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout,
            verify=verify,
            allow_redirects=allow_redirects,
        )
        if not response.status_code == requests.codes.ok:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        log.error(e)
        raise

    return response


def apkmonk_parse_app_details(soup):
    """Extracts an app's details from its info page.
    :param soup: a strained BeautifulSoup object of an app
    :return: a dictionary of app details
    """
    title = soup.select_one('div[class="col l9 s8"] h1[class="hide-on-med-and-down"]').text

    description_soup = soup.select_one('p[id="descr"]')
    if description_soup:
        description = "\n".join(description_soup.stripped_strings)
    else:
        description = None

    data = {
        "title": title,
        "description": description,
    }
    return data


def apkpure_parse_app_details(soup):
    title = soup.select_one('div[class="title-like"]').text
    description_soup = soup.select_one('div[itemprop="description"]')

    if description_soup:
        description = "\n".join(description_soup.stripped_strings)
    else:
        description = None

    data = {
        "title": title,
        "description": description,
    }
    return data


def xpose_repo_parse_app_details(soup):
    title = soup.select_one('h1[id="page-title"]').text.strip()
    print(title)
    description_soup = soup.select_one('div[class="field-item even"]')

    if description_soup:
        description = "\n".join(description_soup.stripped_strings)
        print(description)
    else:
        description = None

    data = {
        "title": title,
        "description": description,
    }
    return data


def parse_app_details(soup, website="apkmonk"):
    """
    Extracts an app's details from its info page.
    :param soup: a strained BeautifulSoup object of an app
    :param website: website to crawl from
    :return: a dictionary of app details
    """
    if website == "apkmonk":
        return apkmonk_parse_app_details(soup)
    elif website == "apkpure":
        return apkpure_parse_app_details(soup)
    elif website == "xpose repo":
        return xpose_repo_parse_app_details(soup)
    pass

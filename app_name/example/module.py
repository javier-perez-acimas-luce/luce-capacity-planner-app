import requests
from flask import abort

from app_name.utils.logger import logger


def get_url_content(url):
    """
    Gets url page content
    @param url: string URL
    @return: requests.Response object
    @raise: HTTPError
    """
    logger.debug(f"Getting content from {url}")
    response = requests.get(url)
    logger.debug(f"Response status code: {response.status_code}")
    if response.status_code != 200:
        abort(response.status_code, response.reason)
    logger.debug(f"Response content: {response.text}")
    return response

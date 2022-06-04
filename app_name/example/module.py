import requests
from flask import abort


def get_url_content(url):
    """
    Gets url page content
    @param url: string URL
    @return: requests.Response object
    @raise: HTTPError
    """
    response = requests.get(url)
    if response.status_code != 200:
        abort(response.status_code, response.reason)
    return response

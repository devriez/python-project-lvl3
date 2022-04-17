from urllib.parse import urlparse
import re
import os
import requests
from page_loader.logger import get_logger
from urllib.parse import urljoin

logger = get_logger(__name__)


def make_dashname_from_url(url):
    '''
    All characters in URL except letters and numbers are replaced with '-'.
    If the web page - '.html' appended at the end of the name.
    If the local resource - '.{extension}' left at the end of the name.
    Parameters:
        url - page or local source URL
    Return: modified name
    '''
    url_without_ext, ext = os.path.splitext(url)
    url_object = urlparse(url_without_ext)

    if not (url_object.path):
        url_without_scheme = url_object.netloc + ext
    else:
        url_without_scheme = url_object.netloc + url_object.path

    url_normilized = re.sub('[^a-zA-Z0-9]', '-', url_without_scheme)

    if not (url_object.path) or not ext:
        return url_normilized + '.html'
    else:
        return url_normilized + ext


def make_absolute_url(root_url, source_url):
    '''
    Make absolute url.
    Parameters:
        root_url - web pagr root directory
        source_url - relative and absolute url
    Return: absolute url
    '''

    if root_url[-1] != '/':
        root_url += '/'

    return urljoin(root_url, source_url)


def file_save(content, path):
    '''
    Save content to file.
    Parametrs:
        content - content to save
        path - file path for saving
    '''
    try:
        with open(path, 'wb') as f:
            f.write(content)
    except FileNotFoundError:
        msg = f"Invalid path to save file: {path}"
        logger.error(msg)
        raise FileNotFoundError(msg)
    except PermissionError:
        msg = f"No permission to save file: {path}"
        logger.error(msg)
        raise PermissionError(msg)
    logger.info('Source saved to file')


def is_link_to_page(link, page):
    '''
    Checks if a link leads to the web page.
    Parameters:
        link - absolute or relative url
        page - page url
    Return: true or false
    '''
    link_netloc = urlparse(link).netloc
    page_netloc = urlparse(page).netloc
    return (link_netloc == page_netloc) or (len(link_netloc) == 0)


def make_dir(path):
    '''
    Creating directory
    Parameters:
        path - directory path
    '''
    try:
        os.mkdir(path)
    except PermissionError:
        msg = f'No permission to create directory {path}'
        logger.error(msg)
        raise PermissionError(msg)
    except FileNotFoundError:
        msg = f"Invalid path for local resources folder: {path}"
        logger.error(msg)
        raise FileNotFoundError(msg)


def read_page(url):
    '''
    Read web page.
    Parameters:
        url - page url
    Return: requst object
    '''
    r = requests.get(url)
    if r.status_code != 200:
        msg = f"Request to {url} returned: {r.status_code} {r.reason}"
        logger.error(msg)
        raise ConnectionError(msg)
    return r

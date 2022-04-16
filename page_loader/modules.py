from urllib.parse import urlparse
import re
import os
import requests
from page_loader.logger import get_logger
from urllib.parse import urljoin

logger = get_logger(__name__)


def make_dashname_from_url(url):
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


def make_file_url_absolute(page_url, file_url):

    if page_url[-1] != '/':
        page_url += '/'

    return urljoin(page_url, file_url)


def file_save(content, path):
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
    link_netloc = urlparse(link).netloc
    page_netloc = urlparse(page).netloc
    return (link_netloc == page_netloc) or (len(link_netloc) == 0)


def make_dir(path):
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
    r = requests.get(url)
    if r.status_code != 200:
        msg = f"Request to {url} returned: {r.status_code} {r.reason}"
        logger.error(msg)
        raise ConnectionError(msg)
    return r

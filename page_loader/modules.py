from urllib.parse import urlparse
import re
import os
import requests
from page_loader.logger import get_logger

logger = get_logger(__name__)


def make_dashname_from_url(url):
    url_without_ext, ext = os.path.splitext(url)
    url_object = urlparse(url_without_ext)

    if len(url_object.scheme) == 0:
        url_without_ext = 'https://' + url_without_ext

    url_object = urlparse(url_without_ext)

    if len(url_object.path) == 0:
        url_without_scheme = url_object.netloc + ext
    else:
        url_without_scheme = url_object.netloc + url_object.path

    url_normilized = re.sub('[^a-zA-Z0-9]', '-', url_without_scheme)

    return url_normilized


def make_saved_file_name(file_url, page_url):
    file_url_without_ext, ext = os.path.splitext(file_url)

    file_url_object = urlparse(file_url)
    file_netloc = file_url_object.netloc
    page_url_object = urlparse(page_url)
    page_netloc = page_url_object.netloc

    if file_netloc == page_netloc:
        return (make_dashname_from_url(file_url_without_ext) + ext)

    return (make_dashname_from_url(page_netloc)
            + make_dashname_from_url(file_url_without_ext)  # noqa: W503
            + ext)  # noqa: W503


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

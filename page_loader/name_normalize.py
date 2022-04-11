from urllib.parse import urlparse
import re
import os


def normalize_page_name(url):
    url_without_ext, _ = os.path.splitext(url)
    url_object = urlparse(url_without_ext)
    url_without_scheme = url_object.netloc + url_object.path
    url_normilized_without_ext = re.sub('[^a-zA-Z0-9]', '-', url_without_scheme)
    return url_normilized_without_ext + '.html'

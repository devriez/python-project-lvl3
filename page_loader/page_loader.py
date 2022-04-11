import requests
import os
from page_loader.name_normalize import normalize_page_name


def download(url, dir=os.getcwd()):
    result_file_name = normalize_page_name(url)
    result_file_path = os.path.join(dir, result_file_name)
    result_file = open(result_file_path, 'w')

    r = requests.get(url)
    result_file.write(r.text)

    return result_file_path

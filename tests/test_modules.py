from page_loader.modules import file_save, make_dashname_from_url
from page_loader.modules import make_saved_file_name
from page_loader.modules import is_link_to_page
from page_loader.modules import make_dir
import pytest
import os


def test_make_dashname_from_url():
    url1 = 'https://en.wikipedia.org/wiki/Peace' 
    normalized_url1 = 'en-wikipedia-org-wiki-Peace.html'
    url2 = 'https://en.wikipedia.org/wiki/Peace.html' 
    normalized_url2 = 'en-wikipedia-org-wiki-Peace.html'
    url3 = 'https://en.wikipedia.org:80/wiki/Peace.html' 
    normalized_url3 = 'en-wikipedia-org-80-wiki-Peace.html'

    assert make_dashname_from_url(url1) + '.html' == normalized_url1
    assert make_dashname_from_url(url2) + '.html' == normalized_url2
    assert make_dashname_from_url(url3) + '.html' == normalized_url3


def test_make_saved_file_name():
    page_url = 'https://ru.hexlet.io/courses'

    file_url = "/assets/professions/nodejs.png"
    result = 'ru-hexlet-io-assets-professions-nodejs.png'
    assert make_saved_file_name(file_url, page_url) == result

    file_url = "https://ru.hexlet.io/packs/js/runtime.js"
    result = 'ru-hexlet-io-packs-js-runtime.js'
    assert make_saved_file_name(file_url, page_url) == result
  

def test_is_link_to_our_page():
    link1 = 'https://cdn2.hexlet.io/assets/menu.css'
    link2 = "/assets/application.css"
    link3 = "https://ru.hexlet.io/packs/js/runtime.js"
    link4 = "https://hexlet.io/packs/js/runtime.js"
    url = 'https://ru.hexlet.io/courses'
    assert is_link_to_page(link2, url)
    assert is_link_to_page(link3, url)
    assert not is_link_to_page(link1, url)
    assert not is_link_to_page(link4, url)


def test_make_dir_doesnt_exist():
    path = os.path.join(os.getcwd(), '/some/wrong/dirrectory')
    with pytest.raises(FileNotFoundError):
        make_dir(path)


def test_file_save_wrong_path():
    path = os.path.join(os.getcwd(), '/some/wrong/dirrectory')
    with pytest.raises(FileNotFoundError):
        file_save('hello', path)

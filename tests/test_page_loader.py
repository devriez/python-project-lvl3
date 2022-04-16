from page_loader.page_loader import download
import os
import requests_mock
import tempfile
import pytest


def test_dowload_page_html(requests_mock):
    web_page = 'https://hexlet.io/courses'
    response_text = '<div>\n test\n</div>'
    requests_mock.get(web_page, text=response_text)

    with tempfile.TemporaryDirectory() as temp_dir:
        result_path = os.path.join(temp_dir, 'hexlet-io-courses.html')
        download(web_page, temp_dir)

        with open(result_path, 'r') as f:
            assert f.read() == response_text


def test_dowload_page_with_local_resources():
    with requests_mock.mock() as m:
        host = 'https://ru.hexlet.io'
        address = host + '/courses'

        with open('tests/fixtures/index.html', 'r') as f:
            m.get(address, text=f.read())

        with open('tests/fixtures/index.css', 'r') as f:
            request_address = host + '/assets/application.css'
            result_css_content = f.read()
            m.get(request_address, text=result_css_content)

        with open('tests/fixtures/index.js', 'r') as f:
            request_address = host + '/packs/js/runtime.js'
            result_js_content = f.read()
            m.get(request_address, text=result_js_content)

        with open('tests/fixtures/index.png', 'rb') as f:
            request_address = host + '/assets/professions/nodejs.png'
            result_bin_content = f.read()
            m.get(request_address, content=result_bin_content)

        with open('tests/fixtures/result.html', 'r') as f:
            result_html_content = f.read()

        with tempfile.TemporaryDirectory() as tmpdirname:
            download(address, tmpdirname)#, logging.DEBUG)

            result_html_path = os.path.join(
                tmpdirname, 'ru-hexlet-io-courses.html'
            )
            with open(result_html_path, 'r') as f:
                assert f.read() == result_html_content

            result_css_path = os.path.join(
                tmpdirname, 
                'ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css'
            )
            with open(result_css_path, 'r') as f:
                assert f.read() == result_css_content

            result_js_path = os.path.join(
                tmpdirname, 
                'ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js'
            )
            with open(result_js_path, 'r') as f:
                assert f.read() == result_js_content

            result_bin_path = os.path.join(
                tmpdirname, 
                'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png'
            )
            with open(result_bin_path, 'rb') as f:
                assert f.read() == result_bin_content


def test_dowload_page_html_status_code_100(requests_mock):
    web_page = 'https://hexlet.io/courses'
    response_text = '<div>\n test\n</div>'
    requests_mock.get(web_page, text=response_text, status_code = 100)

    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(ConnectionError):
            download(web_page, temp_dir)

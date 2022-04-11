from page_loader.page_loader import download
import os
import requests_mock
import tempfile
from page_loader.name_normalize import normalize_page_name

WEB_PAGE_URL = 'https://en.wikipedia.org/wiki/Peace'
MOCK_TEXT_PATH = 'tests/fixtures/file_content.txt'

def test_dowload_file_name(requests_mock):
    mock_text = open(MOCK_TEXT_PATH).read()
    normalized_page_name = normalize_page_name(WEB_PAGE_URL)

    with tempfile.TemporaryDirectory() as temp_dir:
        requests_mock.get(WEB_PAGE_URL, text=mock_text)
        etalon_path = os.path.join(temp_dir, normalized_page_name)

        file_path = download(WEB_PAGE_URL, temp_dir)
        file = open(file_path)
    
        assert etalon_path == file_path
        assert mock_text == file.read()

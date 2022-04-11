from page_loader.name_normalize import normalize_page_name


def test_normilize_page_name():
    url1 = 'https://en.wikipedia.org/wiki/Peace' 
    normalized_url1 = 'en-wikipedia-org-wiki-Peace.html'
    url2 = 'https://en.wikipedia.org/wiki/Peace.html' 
    normalized_url2 = 'en-wikipedia-org-wiki-Peace.html'
    url3 = 'https://en.wikipedia.org:80/wiki/Peace.html' 
    normalized_url3 = 'en-wikipedia-org-80-wiki-Peace.html'

    assert normalize_page_name(url1) == normalized_url1
    assert normalize_page_name(url2) == normalized_url2
    assert normalize_page_name(url3) == normalized_url3
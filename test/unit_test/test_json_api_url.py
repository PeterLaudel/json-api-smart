from src.json_api_url import JsonApiUrl
from urllib.parse import quote


def test_find_url():
    json_api_url = JsonApiUrl('http://base/', 'articles')
    assert json_api_url.find(1) == 'http://base/articles/1'


def test_all_url():
    json_api_url = JsonApiUrl('http://base/', 'articles')
    assert json_api_url.all() == 'http://base/articles'


def test_all_url_with_filter():
    json_api_url = JsonApiUrl('http://base/', 'articles')
    json_api_url.add_filter("hello", "you")
    assert json_api_url.all() == 'http://base/articles?filter%5Bhello%5D=you'


def test_all_url_with_query():
    json_api_url = JsonApiUrl('http://base/', 'articles')
    json_api_url.add_query("hello", "you")
    assert json_api_url.all() == 'http://base/articles?hello=you'

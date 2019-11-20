from src import JsonApiResource, resource_id, attribute
import requests_mock
import os


class Article(JsonApiResource):
    id: str = resource_id()
    title: str = attribute()


def test_response():
    with requests_mock.Mocker() as m, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "response.json"),
                                           "r") as f:
        m.get('http://baseurl.com/articles?price=5&filter[haha]=7', text=f.read())
        assert Article.with_params(price=5).where(haha=7).all()[0].title == 'JSON:API paints my bikeshed!'

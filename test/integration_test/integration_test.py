from src import JsonApiResource, resource_id, attribute
import requests_mock
from typing import Optional
from datetime import date
import os
import dataclasses


class Article(JsonApiResource):
    id: str = resource_id()
    title: str = attribute()
    author: int = attribute()
    some_date: date = attribute(decoder=date.fromisoformat, encoder=date.isoformat)
    some_optional: Optional[int] = attribute(default=None)


def current_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)))


def test_response():
    with requests_mock.Mocker() as m, open(current_dir() + "/response.json", "r") as f:
        m.get("http://baseurl.com/articles?price=5&filter[haha]=7", text=f.read())
        article = Article.with_params(price=5).where(haha=7).all()[0]
        assert article.title == "JSON:API paints my bikeshed!"
        assert article.author == 1
        assert article.some_date == date(2019, 7, 3)
        assert article.some_optional == None

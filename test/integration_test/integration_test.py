from src import JsonApiResource, resource_id, attribute, relationship
import requests_mock
from typing import Optional
from datetime import date
import os


class People(JsonApiResource):
    id: str = resource_id()
    first_name: str = attribute()
    last_name: str = attribute()
    twitter: str = attribute()


class Article(JsonApiResource):
    id: str = resource_id()
    title: str = attribute()
    number: int = attribute()
    some_date: date = attribute(decoder=date.fromisoformat, encoder=date.isoformat)
    some_optional: Optional[int] = attribute(default=None)
    author: People = relationship()


def current_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)))


def test_response():
    with requests_mock.Mocker() as m, open(current_dir() + "/response.json", "r") as f:
        m.get("http://baseurl.com/articles?price=5&filter[haha]=7", text=f.read())
        article = Article.with_params(price=5).where(haha=7).all()[0]

        assert article.title == "JSON:API paints my bikeshed!"
        assert article.number == 1
        assert article.some_date == date(2019, 7, 3)
        assert article.some_optional is None
        assert article.author == People(
            id="9", first_name="Dan", last_name="Gebhardt", twitter="dgeb"
        )

from src import JsonApiResource, resource_id, attribute, relationship
import requests_mock
from typing import Optional, List
from datetime import date
import os


class BaseResource(JsonApiResource):
    @classmethod
    def base_url(cls) -> str:
        return "http://baseurl.com/"


class People(BaseResource):
    id: str = resource_id()
    first_name: str = attribute()
    last_name: str = attribute()
    twitter: str = attribute()


class Comment(BaseResource):
    id: str = resource_id()
    body: str = attribute()


class Article(BaseResource):
    id: str = resource_id()
    title: str = attribute()
    number: int = attribute()
    some_date: date = attribute(decoder=date.fromisoformat)
    comments: List[Comment] = relationship()
    some_optional: Optional[int] = attribute()
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
        assert article.author.id == "9"
        assert article.author.first_name == "Dan"
        assert article.author.last_name == "Gebhardt"
        assert article.author.twitter == "dgeb"
        assert article.comments[0].id == "5"
        assert article.comments[0].body == "First!"
        assert article.comments[1].id == "12"
        assert article.comments[1].body == "I like XML better"

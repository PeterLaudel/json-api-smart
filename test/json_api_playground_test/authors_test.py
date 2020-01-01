from src import JsonApiResource, resource_id, attribute, relationship
from datetime import date
from typing import List


class BaseResource(JsonApiResource):
    @classmethod
    def base_url(cls) -> str:
        return "http://jsonapiplayground.reyesoft.com/v2/"


class Author(BaseResource):
    id: str = resource_id()
    name: str = attribute()
    birthplace: str = attribute()
    date_of_birth: date = attribute(decoder=date.fromisoformat)
    date_of_death: date = attribute(decoder=date.fromisoformat)
    books: List['Book'] = relationship()
    photos: List['Photo'] = relationship()


class Photo(BaseResource):
    id: str = resource_id()


class Book(BaseResource):
    id: str = resource_id()


def test_something():
    authors = Author.all()

    print(authors[0].books)

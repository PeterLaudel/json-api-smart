[![Build Status](https://travis-ci.org/NilssonPL/json-api-smart.svg?branch=master)](https://travis-ci.org/NilssonPL/json-api-smart)
[![Coverage Status](https://coveralls.io/repos/github/NilssonPL/json-api-smart/badge.svg?branch=master)](https://coveralls.io/github/NilssonPL/json-api-smart?branch=master)
# Json API Smart
Json API Smart is your smart JSON::API client.

````json
{
  "data": {
    "type": "articles",
    "id": "101",
    "attributes": {
      "title": "JSON:API paints my bikeshed!",
      "number": 1,
      "some_date": "2019-07-03",
      "some_optional": null
    },
    "relationships": {
      "author": {
        "links": {
          "self": "http://example.com/articles/1/relationships/author",
          "related": "http://example.com/articles/1/author"
        },
        "data": {
          "type": "peoples",
          "id": "9"
        }
      }
    },
    "links": {
      "self": "http://example.com/articles/1"
    }
  },
  "included": [{
    "type": "peoples",
    "id": "9",
    "attributes": {
      "first_name": "Dan"
    },
    "links": {
      "self": "http://example.com/people/9"
    }
  }]
}
````
Can be represtend by following entities:
```python
class BaseResource(JsonApiResource):
    @classmethod
    def base_url(cls) -> str:
        return "http://baseurl.com/"

class People(BaseResource):
    id: str = resource_id()
    first_name: str = attribute()

class Article(BaseResource):
    id: str = resource_id()
    title: str = attribute()
    number: int = attribute()
    some_date: date = attribute(decoder=date.fromisoformat)
    some_optional: Optional[int] = attribute()
    author: People = relationship()
```

Query it with:

````python
# http://baseurl.com/articles/101
article = Article.find("101")
article.id # 101
article.title # JSON:API paints my bikeshed!
article.number # 1
article.some_optional # None
article.author.id # "9"
article.author.first_name # "Dan"
````




[![Build Status](https://travis-ci.org/NilssonPL/json-api-smart.svg?branch=master)](https://travis-ci.org/NilssonPL/json-api-smart)
[![Coverage Status](https://coveralls.io/repos/github/NilssonPL/json-api-smart/badge.svg?branch=master)](https://coveralls.io/github/NilssonPL/json-api-smart?branch=master)
# Json API Smart

Json Api smart is your smart json api client.

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

# Query resources

Call your resources by building chains:

````python
# http://baseurl.com/articles
articles = Article.all()

# http://baseurl.com/articles?price=5
articles = Article.with_params(price=5).all()

# http://baseurl.com/articles?filter[author]=101
articles = Article.where(author=101).all()

# http://baseurl.com/articles/101
articles = Article.find("101")

````




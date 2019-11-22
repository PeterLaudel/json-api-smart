from typing import List, Tuple, Optional, Union, Dict, Generic, Type, TypeVar, Sequence
import inflect
import requests
from urllib.parse import urljoin, urlencode
from .json_api_url import JsonApiUrl

U = TypeVar("U")

engine = inflect.engine()

QueryTypes = Union[str, int, Sequence[str], Sequence[int]]


def _value(value: QueryTypes) -> str:
    if isinstance(value, str):
        return value

    if isinstance(value, int):
        return str(value)

    return ",".join(value)


class JsonApiRequest(Generic[U]):
    def __init__(self, cls: Type[U]):
        self.__cls: Type[U] = cls
        self.__json_api_url = JsonApiUrl(
            cls.base_url(),
            engine.plural(text=cls.__name__.lower())
        )

    def find(self, resource_id: Union[str, int]) -> U:
        response = requests.get(self.__json_api_url.find(resource_id)).json()
        return self.__cls(response["data"])

    def all(self) -> List[U]:
        response = requests.get(url=self.__json_api_url.all()).json()
        response_models = []
        for model in response["data"]:
            response_models.append(self.__cls(model))
        return response_models

    def with_params(self, **kwargs: QueryTypes) -> "JsonApiRequest":
        for key, value in kwargs.items():
            self.__json_api_url.add_query(key, value)

        return self

    def where(self, **kwargs: QueryTypes) -> "JsonApiRequest":
        for key, value in kwargs.items():
            self.__json_api_url.add_filter(key, value)

        return self

    def __attributes(self, json_response) -> Dict:
        return {
            key: value
            for key, value in json_response["attributes"].items()
            if key in set(self.__cls.attributes())
        }

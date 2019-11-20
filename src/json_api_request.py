from typing import List, Tuple, Optional, Union, Dict, Generic, Type, TypeVar, Sequence
import inflect
import requests
from urllib.parse import urljoin, urlencode

U = TypeVar("U")

engine = inflect.engine()

QueryTypes = Union[str, int, Sequence[str], Sequence[int]]


def _value(value: QueryTypes) -> str:
    if isinstance(value, str):
        return value

    if isinstance(value, int):
        return str(value)

    return ','.join(value)


class JsonApiRequest(Generic[U]):

    def __init__(self, cls: Type[U]):
        self.__resource = engine.plural(text=cls.__name__.lower())
        self.__cls: Type[U] = cls
        self.__id: Optional[int] = None
        self.__filter: List[Tuple[str, Union[str, int, List]]] = []
        self.__params: Dict[str, str] = {}

    def find(self, object_id: int) -> U:
        self.__id = object_id
        response = requests.get(self.__build_url()).json()
        return self.__cls(response["data"][0]["id"], response["data"][0]["attributes"]["title"])

    def all(self) -> List[U]:
        url = self.__build_url()
        response = requests.get(url=url).json()
        response_models = []
        for model in response['data']:
            response_models.append(self.__cls(model["id"], model["attributes"]["title"]))
        return response_models

    def with_params(self, **kwargs: QueryTypes) -> "JsonApiRequest":
        for key, value in kwargs.items():
            self.__add_params(key, _value(value))

        return self

    def where(self, **kwargs: QueryTypes) -> "JsonApiRequest":
        for key, value in kwargs.items():
            self.__add_params("filter[{}]".format(key), _value(value))

        return self

    def __attributes(self, json_response) -> Dict:
        return {
            key: value
            for key, value in json_response['attributes'].items()
            if key in set(self.__cls.attributes())
        }

    def __add_params(self, key: str, value: str):
        self.__params[key] = value

    def __build_url(self):
        url = urljoin(self.__cls.base_url(), self.__resource)
        if self.__id:
            url = urljoin(url, self.__resource)
        if len(self.__params) > 0:
            url += '?' + urlencode(self.__params)

        return url

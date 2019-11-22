from typing import Union, Sequence, Dict
from urllib.parse import urljoin, urlencode

QueryTypes = Union[str, int, Sequence[str], Sequence[int]]


def _value(value: QueryTypes) -> str:
    if isinstance(value, str):
        return value

    if isinstance(value, int):
        return str(value)

    return ",".join(value)


class JsonApiUrl:

    def __init__(self, base_url: str, resource: str):
        self.__resource = resource
        self.__base_url = base_url
        self.__params: Dict[str, str] = dict()

    def find(self, resource_id: Union[str, int]) -> str:
        path = self.__resource + "/" + str(resource_id)
        return urljoin(self.__base_url, path)

    def all(self) -> str:
        url = urljoin(self.__base_url, self.__resource)
        if len(self.__params) > 0:
            url += "?" + urlencode(self.__params)
        return url

    def add_filter(self, key: str, value: QueryTypes):
        self.__params["filter[{}]".format(key)] = _value(value)

    def add_query(self, key: str, value: QueryTypes):
        self.__params[key] = _value(value)

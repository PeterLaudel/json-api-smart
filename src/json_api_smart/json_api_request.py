from typing import List, Union, Generic, Type, TypeVar, Sequence
import requests
from .json_api_url import JsonApiUrl
from .json_api_call_context import JsonApiCallContext
from .json_api_resource_base import JsonApiResourceBase
from .types import QueryTypes


class JsonApiRequest:
    def __init__(self, cls: Type[JsonApiResourceBase]):
        self.__cls = cls
        self.__json_api_url = JsonApiUrl(cls.base_url(), cls.resource_name())

    def find(self, resource_id: Union[str, int]) -> JsonApiResourceBase:
        response = requests.get(self.__json_api_url.find(resource_id)).json()
        return self.__cls(self.__json_api_response(response["data"], response))

    def all(self) -> List[JsonApiResourceBase]:
        response = requests.get(url=self.__json_api_url.all()).json()
        response_models = []
        for model in response["data"]:
            response_models.append(
                self.__cls(self.__json_api_response(model, response))
            )
        return response_models

    def with_params(self, **kwargs: QueryTypes) -> "JsonApiRequest":
        for key, value in kwargs.items():
            self.__json_api_url.add_query(key, value)

        return self

    def where(self, **kwargs: QueryTypes) -> "JsonApiRequest":
        for key, value in kwargs.items():
            self.__json_api_url.add_filter(key, value)

        return self

    @staticmethod
    def __json_api_response(data, response) -> JsonApiCallContext:
        return JsonApiCallContext(data=data, included=response.get("included", None))

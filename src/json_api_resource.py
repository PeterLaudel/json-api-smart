from typing import List, Dict, Type, TypeVar
from .json_api_request import JsonApiRequest, QueryTypes
from .attribute import Attribute

H = TypeVar("H")


def get_attribute_entry(response, key):
    return response["attributes"].get(key, None)


class JsonApiResource:
    def __init__(self, json_api_response=None, **kwargs):
        if json_api_response is not None:
            self.id = json_api_response["id"]
            for key, value in self.attributes().items():
                attribute = get_attribute_entry(json_api_response, key)
                attribute_config = getattr(self, key)
                setattr(self, key, attribute_config.handle_value(attribute))
        else:
            self.__dict__.update(kwargs)

    @staticmethod
    def base_url() -> str:
        return "http://baseurl.com"

    @classmethod
    def find(cls: Type[H], object_id: int) -> H:
        return JsonApiRequest(cls).find(object_id=object_id)

    @classmethod
    def all(cls: Type[H]) -> List[H]:
        return JsonApiRequest(cls).all()

    @classmethod
    def with_params(cls: Type[H], **kwargs: QueryTypes) -> JsonApiRequest:
        return JsonApiRequest(cls).with_params(**kwargs)

    @classmethod
    def where(cls: Type[H], **kwargs: QueryTypes):
        return JsonApiRequest(cls).with_params(**kwargs)

    @classmethod
    def attributes(cls: Type[H]) -> Dict[str, type]:
        return {
            key: value
            for key, value in cls.__annotations__.items()
            if type(getattr(cls, key)) is Attribute
        }

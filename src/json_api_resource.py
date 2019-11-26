from typing import List, Dict, Type, TypeVar, Optional
from .json_api_request import JsonApiRequest, QueryTypes
from .attribute import Attribute
from .relationship import Relationship
from .json_api_call_context import JsonApiCallContext
from .json_api_resource_builder import build_resource
from .json_api_resource_base import JsonApiResourceBase
import inflect
import re

H = TypeVar("H", bound="JsonApiResource")

engine = inflect.engine()

first_cap_re = re.compile("(.)([A-Z][a-z]+)")
all_cap_re = re.compile("([a-z0-9])([A-Z])")


def convert(name):
    s1 = first_cap_re.sub(r"\1-\2", name)
    return all_cap_re.sub(r"\1-\2", s1).lower()


class JsonApiResource(JsonApiResourceBase):
    def __init__(
        self, json_api_call_context: Optional[JsonApiCallContext] = None, **kwargs
    ):
        if json_api_call_context is not None:
            build_resource(json_api_call_context, self)
        else:
            self.__dict__.update(kwargs)

    @staticmethod
    def base_url() -> str:
        raise NotImplementedError("Implement this in your base class")

    @classmethod
    def find(cls: Type[H], resource_id: int) -> H:
        return JsonApiRequest(cls).find(resource_id=resource_id)

    @classmethod
    def all(cls: Type[H]) -> List[H]:
        return JsonApiRequest(cls).all()

    @classmethod
    def with_params(cls: Type[H], **kwargs: QueryTypes) -> JsonApiRequest:
        return JsonApiRequest(cls).with_params(**kwargs)

    @classmethod
    def where(cls: Type[H], **kwargs: QueryTypes):
        return JsonApiRequest(cls).where(**kwargs)

    @classmethod
    def attributes(cls: Type[H]) -> List[str]:
        return [
            key
            for key, value in cls.__annotations__.items()
            if type(getattr(cls, key)) is Attribute
        ]

    @classmethod
    def relationships(cls: Type[H]) -> List[str]:
        return [
            key
            for key, value in cls.__annotations__.items()
            if type(getattr(cls, key)) is Relationship
        ]

    @classmethod
    def resource_name(cls: Type[H]) -> str:
        return engine.plural(convert(cls.__name__))

from typing import List, Type, TypeVar, Optional
from inflect import engine as create_engine
import re

from .attribute import Attribute
from .relationship import Relationship
from .resource_id import ResourceId

from .json_api_request import JsonApiRequest
from .json_api_call_context import JsonApiCallContext
from .json_api_resource_builder import build_resource
from .json_api_resource_base import JsonApiResourceBase

from .types import QueryTypes

H = TypeVar("H", bound=JsonApiResourceBase)

engine = create_engine()

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
    def find(cls: Type[JsonApiResourceBase], resource_id: int) -> JsonApiResourceBase:
        return JsonApiRequest(cls).find(resource_id=resource_id)

    @classmethod
    def all(cls: Type[JsonApiResourceBase]) -> List[JsonApiResourceBase]:
        return JsonApiRequest(cls).all()

    @classmethod
    def with_params(
        cls: Type[JsonApiResourceBase], **kwargs: QueryTypes
    ) -> JsonApiRequest:
        return JsonApiRequest(cls).with_params(**kwargs)

    @classmethod
    def where(cls: Type[JsonApiResourceBase], **kwargs: QueryTypes) -> JsonApiRequest:
        return JsonApiRequest(cls).where(**kwargs)

    @classmethod
    def attributes(cls: Type[JsonApiResourceBase]) -> List[str]:
        return [
            key
            for key in cls.__annotations__.keys()
            if type(getattr(cls, key)) is Attribute
        ]

    @classmethod
    def relationships(cls: Type[JsonApiResourceBase]) -> List[str]:
        return [
            key
            for key in cls.__annotations__.keys()
            if type(getattr(cls, key)) is Relationship
        ]

    @classmethod
    def resource_id(cls: Type[JsonApiResourceBase]) -> str:
        resource_ids = [
            key
            for key in cls.__annotations__.keys()
            if type(getattr(cls, key)) is ResourceId
        ]

        if len(resource_ids) > 1:
            raise AttributeError("Only one resource id per resource object allowed")

        if len(resource_ids) == 0:
            raise AttributeError("Resource object needs a defined resource id")

        return resource_ids[0]

    @classmethod
    def resource_name(cls: Type[JsonApiResourceBase]) -> str:
        return engine.plural(convert(cls.__name__))

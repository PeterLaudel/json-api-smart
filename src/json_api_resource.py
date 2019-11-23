from typing import List, Dict, Type, TypeVar, Optional
from .json_api_request import JsonApiRequest, QueryTypes
from .attribute import Attribute, MISSING
from .relationship import Relationship
from .json_api_call_context import JsonApiCallContext
import inflect

H = TypeVar("H")

engine = inflect.engine()


class JsonApiResource:
    def __init__(
        self, json_api_call_context: Optional[JsonApiCallContext] = None, **kwargs
    ):
        if json_api_call_context is not None:
            self.id = json_api_call_context.get_id()
            self.__add_attributes(json_api_call_context)
            self.__add_relationships(json_api_call_context)
        else:
            self.__dict__.update(kwargs)

    def __add_attributes(self, json_api_call_context: JsonApiCallContext):
        for key, value in self.attributes().items():
            attribute_config = getattr(self, key)
            attribute = attribute_config.handle_value(
                json_api_call_context.get_attribute(key), value
            )
            setattr(self, key, attribute)

    def __add_relationships(self, json_api_call_context: JsonApiCallContext):
        for key, value in self.relationships().items():
            relationship_entry = json_api_call_context.get_relationship(key)
            include = json_api_call_context.find_in_included(
                value.resource_name(), relationship_entry["data"]["id"]
            )
            setattr(self, key, value(JsonApiCallContext(data=include)))

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

    @classmethod
    def relationships(cls: Type[H]) -> Dict[str, type]:
        return {
            key: value
            for key, value in cls.__annotations__.items()
            if type(getattr(cls, key)) is Relationship
        }

    @classmethod
    def resource_name(cls: Type[H]) -> str:
        return engine.plural(cls.__name__.lower())

    def __eq__(self, other):
        for key in self.attributes().keys():
            if getattr(self, key) != getattr(other, key):
                return False

        return True

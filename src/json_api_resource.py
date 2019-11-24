from typing import List, Dict, Type, TypeVar, Optional
from .json_api_request import JsonApiRequest, QueryTypes
from .attribute import Attribute
from .relationship import Relationship
from .json_api_call_context import JsonApiCallContext
from .type_utils import is_optional
import inflect
import re

H = TypeVar("H", bound="JsonApiResource")

engine = inflect.engine()

first_cap_re = re.compile("(.)([A-Z][a-z]+)")
all_cap_re = re.compile("([a-z0-9])([A-Z])")


def convert(name):
    s1 = first_cap_re.sub(r"\1-\2", name)
    return all_cap_re.sub(r"\1-\2", s1).lower()


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
            if relationship_entry is None:
                raise ValueError("The relationship %s is not missing" % key)
            if relationship_entry["data"] is None:
                if is_optional(value):
                    setattr(self, key, None)
                    continue
                else:
                    raise ValueError(
                        "The relationship %s data entry is 'None' but not optional"
                        % key
                    )

            include = json_api_call_context.find_in_included(
                value.resource_name(), relationship_entry["data"]["id"]
            )
            if include is not None:
                setattr(self, key, value(JsonApiCallContext(data=include)))
            else:
                setattr(self, key, value(id=relationship_entry["data"]["id"]))
                self.__delete_attributes()

    def __delete_attributes(self):
        for key in self.attributes().keys():
            delattr(self, key)

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
    def attributes(cls: Type[H]) -> Dict[str, type]:
        return {
            key: value
            for key, value in cls.__annotations__.items()
            if type(getattr(cls, key)) is Attribute
        }

    @classmethod
    def relationships(cls: Type[H]) -> Dict[str, H]:
        return {
            key: value
            for key, value in cls.__annotations__.items()
            if type(getattr(cls, key)) is Relationship
        }

    @classmethod
    def resource_name(cls: Type[H]) -> str:
        return engine.plural(convert(cls.__name__))

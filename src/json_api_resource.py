from typing import List, Dict, Type, TypeVar, Optional
from .json_api_request import JsonApiRequest, QueryTypes
from .attribute import Attribute, MISSING
from .relationship import Relationship
from .json_api_response import JsonApiResponse
import inflect

H = TypeVar("H")

engine = inflect.engine()


def get_attribute_entry(data, key):
    return data["attributes"].get(key, None)


def get_relationship_entry(data, key):
    return data["relationships"].get(key, None)


def find_in_included(resource_type: str, resource_id: str, included):
    for include in included:
        if include["type"] == resource_type and include["id"] == resource_id:
            return include


def find_attribute(
    data: Dict, key: str, attribute_config: Attribute, attribute_type: Type[H]
) -> H:
    data_attribute = get_attribute_entry(data, key)

    if data_attribute is None and attribute_config.default is not MISSING:
        return attribute_config.default

    if attribute_config.decoder is not None:
        return attribute_config.decoder(data_attribute)

    return attribute_type(data_attribute)


def find_relationship(
    json_api_response: JsonApiResponse, key: str, relationship_type: Type[H],
) -> H:
    data_entry = get_relationship_entry(json_api_response.data, key)
    include = find_in_included(
        relationship_type.resource_name(),
        data_entry['data']["id"],
        json_api_response.included
    )

    return relationship_type(JsonApiResponse(data=include))


class JsonApiResource:
    def __init__(self, json_api_response: Optional[JsonApiResponse] = None, **kwargs):
        if json_api_response is not None:
            self.id = json_api_response.data.get("id", None)
            for key, value in self.attributes().items():
                attribute = find_attribute(
                    json_api_response.data, key, getattr(self, key), value
                )
                setattr(self, key, attribute)

            for key, value in self.relationships().items():
                relationship = find_relationship(json_api_response, key, value)
                setattr(self, key, relationship)
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

from .json_api_call_context import JsonApiCallContext
from .json_api_resource_base import JsonApiResourceBase
from .type_utils import is_optional, is_list
from typing import ForwardRef
from typeguard import check_type
from .json_api_resource_base import JsonApiResourceBase


def all_subclasses(cls=JsonApiResourceBase):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)]
    )


def base_classes():
    return {subclass.__name__: subclass for subclass in all_subclasses()}


def __add_relationship_list(
        key: str,
        json_api_resource: JsonApiResourceBase,
        json_api_call_context: JsonApiCallContext,
):
    relationship_entry = json_api_call_context.get_relationship(key)
    if relationship_entry is None:
        raise ValueError("The relationship %s is missing" % key)
    relationship_list = []
    for relationship in relationship_entry["data"]:
        include = json_api_call_context.find_in_included(
            relationship["type"], relationship["id"]
        )
        value = json_api_resource.__annotations__[key]
        final_type = value.__args__[0]
        if type(final_type) is ForwardRef:
            final_type = base_classes()[final_type.__forward_arg__]

        if include is not None:
            relationship_list.append(
                final_type(JsonApiCallContext(data=include))
            )
        else:
            relationship_list.append(final_type(id=relationship["id"]))

    setattr(json_api_resource, key, relationship_list)


def __add_relationship(
        key: str,
        json_api_resource: JsonApiResourceBase,
        json_api_call_context: JsonApiCallContext,
):
    relationship_entry = json_api_call_context.get_relationship(key)
    if relationship_entry is None:
        raise ValueError("The relationship %s is missing" % key)

    final_type = json_api_resource.__annotations__[key]
    if type(final_type) is ForwardRef:
        final_type = base_classes()[final_type.__forward_arg__]
    if relationship_entry["data"] is None:
        if is_optional(final_type):
            setattr(json_api_resource, key, None)
            return
        else:
            raise ValueError(
                "The relationship %s data entry is 'None' but not optional" % key
            )

    include = json_api_call_context.find_in_included(
        final_type.resource_name(), relationship_entry["data"]["id"]
    )
    if include is not None:
        setattr(json_api_resource, key, final_type(JsonApiCallContext(data=include)))
    else:
        setattr(json_api_resource, key, final_type(id=relationship_entry["data"]["id"]))


def __add_relationships(
        json_api_resource: JsonApiResourceBase, json_api_call_context: JsonApiCallContext
):
    for key in json_api_resource.relationships():
        value = json_api_resource.__annotations__[key]
        if is_list(value):
            __add_relationship_list(key, json_api_resource, json_api_call_context)
        else:
            __add_relationship(key, json_api_resource, json_api_call_context)


def __add_attributes(
        json_api_resource: JsonApiResourceBase, json_api_call_context: JsonApiCallContext
):
    for key in json_api_resource.attributes():
        attribute_config = getattr(json_api_resource, key)
        attribute = json_api_call_context.get_attribute(key)

        if attribute_config.decoder is not None:
            attribute = attribute_config.decoder(attribute)

        value = json_api_resource.__annotations__[key]
        check_type(key, attribute, value)

        setattr(json_api_resource, key, attribute)


def __add_id(
        json_api_resource: JsonApiResourceBase, json_api_call_context: JsonApiCallContext
):
    setattr(
        json_api_resource,
        json_api_resource.resource_id(),
        json_api_call_context.get_id(),
    )


def build_resource(
        json_api_call_context: JsonApiCallContext, json_api_resource: JsonApiResourceBase
):
    __add_id(json_api_resource, json_api_call_context)
    __add_attributes(json_api_resource, json_api_call_context)
    __add_relationships(json_api_resource, json_api_call_context)
    return json_api_resource

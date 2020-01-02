import pytest
from typing import Optional
from datetime import date
from typing import ForwardRef
from src import JsonApiResource, resource_id, attribute, relationship
from src.json_api_call_context import JsonApiCallContext
from src.json_api_resource_builder import build_resource


class BaseResource(JsonApiResource):
    @staticmethod
    def base_url() -> str:
        return "http://some.url"


def test_builds_resource_with_id():
    class Resource(BaseResource):
        id: str = resource_id()

    result = build_resource(JsonApiCallContext(data={"id": "42"}), Resource())

    assert result.id == "42"


def test_builds_resource_with_attributes():
    class Resource(BaseResource):
        id: str = resource_id()
        attribute1: str = attribute()

    result = build_resource(
        JsonApiCallContext(data={"id": "42", "attributes": {"attribute1": "value"}}),
        Resource(),
    )

    assert result.attribute1 == "value"


def test_builds_resource_with_decoded_attributes():
    class Resource(BaseResource):
        id: str = resource_id()
        attribute1: date = attribute(decoder=date.fromisoformat)

    result = build_resource(
        JsonApiCallContext(data={"id": "42", "attributes": {"attribute1": "2019-07-04"}}),
        Resource(),
    )

    assert result.attribute1 == date(2019, 7, 4)


def test_builds_resource_raises_type_error():
    class Resource(BaseResource):
        id: str = resource_id()
        attribute1: str = attribute()

    with pytest.raises(TypeError, match=r".* attribute1 .*"):
        build_resource(
            JsonApiCallContext(data={"id": "42", "attributes": {"attribute1": 1}}),
            Resource(),
        )


def test_builds_resource_with_relationship_not_in_included():
    class Relationship(BaseResource):
        id: str = resource_id()
        attribute1: str = attribute()

    class Resource(BaseResource):
        id: str = resource_id()
        relationship1: Relationship = relationship()

    result = build_resource(
        JsonApiCallContext(
            data={
                "id": "100",
                "relationships": {
                    "relationship1": {"data": {"id": "42", "type": "relationships"}}
                },
            }
        ),
        Resource(),
    )

    assert result.relationship1.id == "42"


def test_build_resource_with_relationship():
    class Relationship(BaseResource):
        id: str = resource_id()
        attribute1: str = attribute()

    class Resource(BaseResource):
        id: str = resource_id()
        relationship1: Relationship = relationship()

    result = build_resource(
        JsonApiCallContext(
            data={
                "id": "100",
                "relationships": {
                    "relationship1": {"data": {"id": "42", "type": "relationships"}}
                },
            },
            included=[
                {
                    "id": "42",
                    "type": "relationships",
                    "attributes": {"attribute1": "value"},
                }
            ],
        ),
        Resource(),
    )

    assert result.relationship1.id == "42"
    assert result.relationship1.attribute1 == "value"


def test_build_resource_with_optional_relationship():
    class Relationship(BaseResource):
        id: str = resource_id()

    class Resource(BaseResource):
        id: str = resource_id()
        relationship1: Optional[Relationship] = relationship()

    result = build_resource(
        JsonApiCallContext(
            data={"id": "100", "relationships": {"relationship1": {"data": None}}}
        ),
        Resource(),
    )

    assert result.relationship1 is None


def test_build_resource_with_non_optional_relationship_raise_error():
    class Relationship(BaseResource):
        id: str = resource_id()

    class Resource(BaseResource):
        id: str = resource_id()
        relationship1: Relationship = relationship()

    with pytest.raises(ValueError, match=r".* relationship1 .*"):
        build_resource(
            JsonApiCallContext(
                data={"id": "100", "relationships": {"relationship1": {"data": None}}}
            ),
            Resource(),
        )


def test_build_resource_raises_if_relationship_is_not_optional():
    class Relationship(BaseResource):
        id: str = resource_id()

    class Resource(BaseResource):
        id: str = resource_id()
        relationship1: Relationship = relationship()

    with pytest.raises(ValueError, match=r".* relationship1 .*"):
        build_resource(
            JsonApiCallContext(data={"id": "100", "relationships": {}}), Resource()
        )

def test_build_resource_with_cyclic_dependency():

    class Resource(BaseResource):
        id: str = resource_id()
        relationship1: ForwardRef("Relationship") = relationship()

    class Relationshup(BaseResource):
        id: str = resource_id()

    result = build_resource(
        JsonApiCallContext(
            data={
                "id": "100",
                "relationships": {
                    "relationship1": {"data": {"id": "42", "type": "relationships"}}
                },
            }
        ),
        Resource(),
    )

    assert result.relationship1.id == "42"


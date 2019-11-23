from src import JsonApiResource, attribute, resource_id, relationship
from src.json_api_call_context import JsonApiCallContext


class BaseResource(JsonApiResource):
    @staticmethod
    def base_url() -> str:
        return "http://some.url"


def test_attributes():
    class Resource(BaseResource):
        attribute1: int = attribute()
        attribute2: str = attribute()

    assert Resource.attributes() == {"attribute1": int, "attribute2": str}


def test_relationships():
    class Relationship(BaseResource):
        id: str = resource_id()

    class Resource(BaseResource):
        id: str = resource_id()
        relationship1: Relationship = relationship()

    assert Resource.relationships() == {"relationship1": Relationship}


def test_resource_name():
    class SomeResource(BaseResource):
        pass

    assert SomeResource.resource_name() == "some-resources"


def test_base_url():
    class Resource(BaseResource):
        pass

    assert Resource.base_url() == "http://some.url"


def test_builds_resource_with_id():
    class Resource(BaseResource):
        id: str = resource_id()

    result = Resource(JsonApiCallContext(data={"id": "42"}))

    assert result.id == "42"


def test_builds_resource_with_attributes():
    class Resource(BaseResource):
        id: str = resource_id()
        attribute1: str = attribute()

    result = Resource(
        JsonApiCallContext(data={"id": "42", "attributes": {"attribute1": "value"}})
    )

    assert result.attribute1 == "value"


def test_builds_resource_with_relationship():
    class Relationship(BaseResource):
        id: str = resource_id()

    class Resource(BaseResource):
        id: str = resource_id()
        relationship1: Relationship = relationship()

    result = Resource(
        json_api_call_context=JsonApiCallContext(
            data={
                "id": "100",
                "relationships": {
                    "relationship1": {"data": {"id": "42", "type": "relationships"}}
                },
            },
            included=[{"id": "42", "type": "relationships"}],
        )
    )

    assert result.relationship1.id == "42"

import pytest
from typing import Optional
from unittest.mock import patch
from src import JsonApiResource, attribute, resource_id, relationship
from src.json_api_call_context import JsonApiCallContext


class BaseResource(JsonApiResource):
    @staticmethod
    def base_url() -> str:
        return "http://some.url"


def test_base_url_raises_not_implemented():
    with pytest.raises(NotImplementedError, match=r"Implement this .*"):
        JsonApiResource.base_url()


@patch("src.json_api_resource.JsonApiRequest")
def test_find(json_api_request_mock):
    BaseResource.find(1)

    json_api_request_mock.return_value.find.assert_called_once_with(resource_id=1)
    json_api_request_mock.assert_called_once_with(BaseResource)


@patch("src.json_api_resource.JsonApiRequest")
def test_all(json_api_request_mock):
    BaseResource.all()

    json_api_request_mock.return_value.all.assert_called_once()
    json_api_request_mock.assert_called_once_with(BaseResource)


@patch("src.json_api_resource.JsonApiRequest")
def test_with_params(json_api_request_mock):
    BaseResource.with_params(a="b", c="d")

    json_api_request_mock.return_value.with_params.assert_called_once_with(a="b", c="d")
    json_api_request_mock.assert_called_once_with(BaseResource)


@patch("src.json_api_resource.JsonApiRequest")
def test_where(json_api_request_mock):
    BaseResource.where(a="b", c="d")

    json_api_request_mock.return_value.where.assert_called_once_with(a="b", c="d")
    json_api_request_mock.assert_called_once_with(BaseResource)


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


def test_builds_resource_with_relationship_not_in_included():
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
            }
        )
    )

    assert result.relationship1.id == "42"


def test_build_resource_with_relationship():
    class Relationship(BaseResource):
        id: str = resource_id()
        attribute1: str = attribute()

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
            included=[
                {
                    "id": "42",
                    "type": "relationships",
                    "attributes": {"attribute1": "value"},
                }
            ],
        )
    )

    assert result.relationship1.id == "42"
    assert result.relationship1.attribute1 == "value"


def test_build_resource_with_optional_relationship():
    class Relationship(BaseResource):
        id: str = resource_id()

    class Resource(BaseResource):
        id: str = resource_id()
        relationship1: Optional[Relationship] = relationship()

    result = Resource(
        json_api_call_context=JsonApiCallContext(
            data={
                "id": "100",
                "relationships": {
                    "relationship1": None
                },
            }
        )
    )

    assert result.relationship1 is None


def test_build_resource_raises_if_relationship_is_not_optional():
    class Relationship(BaseResource):
        id: str = resource_id()

    class Resource(BaseResource):
        id: str = resource_id()
        relationship1: Relationship = relationship()

    with pytest.raises(ValueError, match=r".* relationship1 .*"):
        Resource(
            json_api_call_context=JsonApiCallContext(
                data={
                    "id": "100",
                    "relationships": {
                        "relationship1": None
                    },
                }
            )
        )



def test_build_new_resource():
    class Resource(BaseResource):
        id: str = resource_id()
        attribute1: str = attribute()

    result = Resource(id="42", attribute1="value")

    assert result.id == "42"
    assert result.attribute1 == "value"

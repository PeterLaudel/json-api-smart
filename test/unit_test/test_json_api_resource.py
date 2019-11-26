import pytest
from unittest.mock import patch, Mock, ANY
from src import JsonApiResource, attribute, resource_id, relationship


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

    assert Resource.attributes() == ["attribute1", "attribute2"]


def test_relationships():
    class Relationship(BaseResource):
        id: str = resource_id()

    class Resource(BaseResource):
        id: str = resource_id()
        relationship1: Relationship = relationship()

    assert Resource.relationships() == ["relationship1"]


def test_resource_name():
    class SomeResource(BaseResource):
        pass

    assert SomeResource.resource_name() == "some-resources"


def test_base_url():
    class Resource(BaseResource):
        pass

    assert Resource.base_url() == "http://some.url"


@patch("src.json_api_resource.build_resource")
def test_build_new_resource_from_request(build_resource_mock):
    class Resource(BaseResource):
        id: str = resource_id()

    json_api_call_context = Mock()
    resource = Resource(json_api_call_context=json_api_call_context)

    build_resource_mock.assert_called_once_with(json_api_call_context, resource)


def test_build_new_resource():
    class Resource(BaseResource):
        id: str = resource_id()
        attribute1: str = attribute()

    result = Resource(id="42", attribute1="value")

    assert result.id == "42"
    assert result.attribute1 == "value"


def test_resource_id_raises_error_if_multiple_ids_exist():
    class Resource(BaseResource):
        id1: str = resource_id()
        id2: str = resource_id()

    with pytest.raises(AttributeError, match=r".* one .*"):
        Resource.resource_id()


def test_resource_id_raises_error_if_no_id_exist():
    class Resource(BaseResource):
        attribute1: str = attribute()

    with pytest.raises(AttributeError, match=r".* needs .*"):
        Resource.resource_id()


def test_resource_id_returns_id_name():
    class Resource(BaseResource):
        some_id: str = resource_id()

    assert Resource.resource_id() == "some_id"

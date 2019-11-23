from unittest.mock import Mock, patch
import requests_mock
from src.json_api_request import JsonApiRequest
from src.json_api_response import JsonApiCallContext
import json


@patch("src.json_api_request.JsonApiCallContext")
def test_find_returns_build_type_from_request(json_api_call_context_mock):
    with requests_mock.Mocker() as m:
        m.get("http://base_url.de/articles/1", text=json.dumps({"data": "huhu"}))
        type_mock = Mock(return_value=Mock())
        type_mock.resource_name.return_value = "articles"
        type_mock.base_url.return_value = "http://base_url.de"

        test_json_api_url = JsonApiRequest(type_mock)
        result = test_json_api_url.find(1)

        assert result == type_mock.return_value
        type_mock.assert_called_once_with(json_api_call_context_mock.return_value)


@patch("src.json_api_request.JsonApiCallContext")
def test_all_returns_build_types_from_request(json_api_call_context_mock):
    with requests_mock.Mocker() as m:
        m.get(
            "http://base_url.de/articles", text=json.dumps({"data": ["huhu", "haha"]})
        )
        type_mock = Mock(return_value=Mock())
        type_mock.resource_name.return_value = "articles"
        type_mock.base_url.return_value = "http://base_url.de"

        test_json_api_url = JsonApiRequest(type_mock)
        result = test_json_api_url.all()

        assert result == [type_mock.return_value, type_mock.return_value]
        assert type_mock.call_count == 2
        type_mock.assert_any_call(json_api_call_context_mock.return_value)
        type_mock.assert_any_call(json_api_call_context_mock.return_value)


def test_all_returns_build_types_with_filter_parameter():
    with requests_mock.Mocker() as m:
        m.get(
            "http://base_url.de/articles?filter[type]=some_type",
            text=json.dumps({"data": ["huhu"]}),
        )
        type_mock = Mock(return_value=Mock())
        type_mock.resource_name.return_value = "articles"
        type_mock.base_url.return_value = "http://base_url.de"

        test_json_api_url = JsonApiRequest(type_mock)
        result = test_json_api_url.where(type="some_type").all()

        assert result == [type_mock.return_value]


def test_all_returns_build_types_with_query_parameter():
    with requests_mock.Mocker() as m:
        m.get(
            "http://base_url.de/articles?type=some_type",
            text=json.dumps({"data": ["huhu"]}),
        )
        type_mock = Mock(return_value=Mock())
        type_mock.resource_name.return_value = "articles"
        type_mock.base_url.return_value = "http://base_url.de"

        test_json_api_url = JsonApiRequest(type_mock)
        result = test_json_api_url.with_params(type="some_type").all()

        assert result == [type_mock.return_value]

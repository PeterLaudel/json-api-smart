from unittest.mock import Mock
import requests_mock
from src.json_api_request import JsonApiRequest
import json


def test_find_returns_build_type_from_request():
    with requests_mock.Mocker() as m:
        m.get(
            "http://base_url.de/articles/1",
            text=json.dumps({"data": "huhu"})
        )
        type_mock = Mock(return_value=Mock(), __name__="Article")
        type_mock.base_url.return_value = "http://base_url.de"

        test_json_api_url = JsonApiRequest(type_mock)
        result = test_json_api_url.find(1)

        assert result == type_mock.return_value
        type_mock.assert_called_once_with("huhu")


def test_all_returns_build_types_from_request():
    with requests_mock.Mocker() as m:
        m.get(
            "http://base_url.de/articles",
            text=json.dumps({"data": ["huhu", "haha"]})
        )
        type_mock = Mock(return_value=Mock(), __name__="Article")
        type_mock.base_url.return_value = "http://base_url.de"

        test_json_api_url = JsonApiRequest(type_mock)
        result = test_json_api_url.all()

        assert result == [type_mock.return_value, type_mock.return_value]
        assert type_mock.call_count == 2
        type_mock.assert_any_call("huhu")
        type_mock.assert_any_call("haha")


def test_all_returns_build_types_with_filter_parameter():
    with requests_mock.Mocker() as m:
        m.get(
            "http://base_url.de/articles?filter[type]=some_type",
            text=json.dumps({"data": ["huhu"]}),
        )
        type_mock = Mock(return_value=Mock(), __name__="Article")
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
        type_mock = Mock(return_value=Mock(), __name__="Article")
        type_mock.base_url.return_value = "http://base_url.de"

        test_json_api_url = JsonApiRequest(type_mock)
        result = test_json_api_url.with_params(type="some_type").all()

        assert result == [type_mock.return_value]

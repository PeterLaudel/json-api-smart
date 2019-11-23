from src.json_api_call_context import JsonApiCallContext


def test_get_id():
    json_api_call_context = JsonApiCallContext(data={"id": "2"})
    assert json_api_call_context.get_id() == "2"


def test_get_attribute():
    json_api_call_context = JsonApiCallContext(
        data={"attributes": {"attribute1": "value1"}}
    )
    assert json_api_call_context.get_attribute("attribute1") == "value1"


def test_get_relationship():
    json_api_call_context = JsonApiCallContext(
        data={"relationships": {"author": "some_relationship"}}
    )
    assert json_api_call_context.get_relationship("author") == "some_relationship"


def test_get_relationship_returns_none_if_not_exist():
    json_api_call_context = JsonApiCallContext(
        data={"relationships": {"author": "some_relationship"}}
    )
    assert json_api_call_context.get_relationship("unknown") is None


def test_find_in_included():
    include = {"type": "articles", "id": "100", "attributes": {"attribute1": "value1"}}
    json_api_call_context = JsonApiCallContext(data={}, included=[include])
    assert json_api_call_context.find_in_included("articles", "100") == include


def test_find_in_included_returns_none_if_included_not_set():
    json_api_call_context = JsonApiCallContext(data={})
    assert json_api_call_context.find_in_included("articles", "100") is None


def test_find_in_include_returns_none_not_found():
    include = {"type": "articles", "id": "100", "attributes": {"attribute1": "value1"}}
    json_api_call_context = JsonApiCallContext(data={}, included=[include])
    assert json_api_call_context.find_in_included("bla", "42") is None

from json import dumps as to_json
import pytest
from requests import Session
from requests.adapters import BaseAdapter
from requests.models import PreparedRequest, Response
from requtests import (
    fake_request,
    fake_request_with_response,
    fake_response,
    FakeAdapter,
)


TEST_DATA = "some data"
TEST_URL = "https://api.example.com/some/url"


def test_fake_adapter():
    response = fake_response()
    adapter = FakeAdapter(response)
    assert isinstance(adapter, BaseAdapter)
    assert adapter.send(PreparedRequest()) == response
    assert adapter.close() is None


def test_fake_adapter_with_assert_step():
    response = fake_response()
    adapter = FakeAdapter(
        response,
        assertions=assert_prepared_request(url=TEST_URL, body=TEST_DATA),
    )
    assert adapter.send(build_request(url=TEST_URL, body=TEST_DATA)) == response


def test_fake_adapter_with_failing_assert_step():
    response = fake_response()
    adapter = FakeAdapter(
        response,
        assertions=assert_prepared_request(url=TEST_URL, body=TEST_DATA),
    )
    with pytest.raises(AssertionError, match="assert 'unexpected data' == 'some data'"):
        adapter.send(build_request(url=TEST_URL, body="unexpected data")) == response


def test_fake_adapter_with_multiple_responses():
    response_1 = fake_response(status_code=429)
    response_2 = fake_response()
    adapter = FakeAdapter(
        response_1,
        response_2,
        assertions=assert_prepared_request(url=TEST_URL, body=TEST_DATA),
    )
    request = build_request(url=TEST_URL, body=TEST_DATA)
    assert adapter.send(request) == response_1
    assert adapter.send(request) == response_2


def test_fake_adapter_with_multiple_responses_and_assertions():
    data_1 = TEST_DATA
    data_2 = "some more data"
    response_1 = fake_response(status_code=429)
    response_2 = fake_response()
    adapter = FakeAdapter(
        response_1,
        response_2,
        assertions=[
            assert_prepared_request(url=TEST_URL, body=data_1),
            assert_prepared_request(url=TEST_URL, body=data_2),
        ],
    )
    request_1 = build_request(url=TEST_URL, body=data_1)
    request_2 = build_request(url=TEST_URL, body=data_2)
    assert adapter.send(request_1) == response_1
    assert adapter.send(request_2) == response_2


def test_fake_adapter_mounted_on_session():
    response = fake_response()
    adapter = FakeAdapter(response, assertions=assert_prepared_request(url=TEST_URL))
    session = Session()
    session.mount("https://", adapter)
    assert session.request("GET", TEST_URL) == response


def test_fake_request():
    request = fake_request(
        fake_response(json={"some": "data"}, status_code=418),
        fake_response(json={"status": "created"}, status_code=201),
    )

    assert_response(
        request("GET", "https://api.example.com/endpoint", params={"page": 1}),
        json={"some": "data"},
        status_code=418,
    )

    assert_response(
        request("GET", "https://api.example.com/endpoint", params={"page": 2}),
        json={"status": "created"},
        status_code=201,
    )


def test_fake_request_with_response():
    response_config = {
        "json": {"some": "data"},
        "reason": "some reason",
        "status_code": 418,
        "url": "some url",
    }

    request = fake_request_with_response(**response_config)
    response = request(
        "GET",
        "https://api.example.com/endpoint",
        params={"some": "param"},
        headers={"some": "header"},
    )
    assert_response(response, **response_config)


def test_fake_response_with_json_data():
    response_config = {
        "json": {"error": "Unauthorized"},
        "reason": "Unauthorized",
        "status_code": 401,
        "url": "https://api.example.com/unauthorized",
    }

    response = fake_response(**response_config)
    assert_response(response, **response_config)


def test_fake_response_with_headers():
    response_config = {
        "json": {"error": "Unauthorized"},
        "reason": "Unauthorized",
        "status_code": 401,
        "url": "https://api.example.com/unauthorized",
        "headers": {
            "Date": "Fri, 28 Jan 2022 08:51:56 GMT",
            "Content-Type": "application/json",
        },
    }

    response = fake_response(**response_config)
    assert_response(response, **response_config)


def test_fake_response_with_empty_data():
    response = fake_response(data={})
    assert_response(response, json={})


def test_fake_response_with_empty_json():
    response = fake_response(json={})
    assert_response(response, json={})


def test_fake_response_with_empty_text():
    response = fake_response(text="")
    assert_response(response, text="")


def test_fake_response_with_text():
    response_config = {
        "reason": "Forbidden",
        "status_code": 403,
        "text": "FORBIDDEN",
        "url": "https://api.example.com/forbidden",
    }

    response = fake_response(**response_config)
    assert_response(response, **response_config)


def assert_prepared_request(url=None, body=None):
    def assertions(request, **kwargs):
        assert request.url == url
        assert request.body == body

    return assertions


def assert_response(
    response, json=None, reason=None, status_code=200, text=None, url=None, headers={}
):
    assert type(response) == Response
    assert response.status_code == status_code
    assert response.reason == reason
    assert response.url == url
    assert response.headers == headers
    if json is not None:
        assert response._content == to_json(json).encode()
        assert response.json() == json
    if text is not None:
        assert response._content == text.encode()
        assert response.text == text


def build_request(url=None, body=None):
    request = PreparedRequest()
    request.url = url
    request.body = body
    return request

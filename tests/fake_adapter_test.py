import pytest
from requests import Session
from requests.adapters import BaseAdapter
from requests.models import PreparedRequest
from requtests import FakeAdapter, fake_response
from .test_utils import assert_prepared_request, build_request

TEST_DATA = "some data"
TEST_URL = "https://api.example.com/some/url"


def test_fake_adapter():
    response = fake_response()
    adapter = FakeAdapter(response)
    request = PreparedRequest()
    assert response.request is None
    assert isinstance(adapter, BaseAdapter)
    assert not adapter.closed
    assert adapter.send(request) is response
    assert adapter.close() is None
    assert adapter.closed
    assert response.request is request


def test_fake_adapter_with_assert_step():
    response = fake_response()
    adapter = FakeAdapter(
        response,
        assertions=assert_prepared_request(url=TEST_URL, body=TEST_DATA),
    )
    assert adapter.send(build_request(url=TEST_URL, data=TEST_DATA)) == response


def test_fake_adapter_with_failing_assert_step():
    response = fake_response()
    adapter = FakeAdapter(
        response,
        assertions=assert_prepared_request(url=TEST_URL, body=TEST_DATA),
    )
    with pytest.raises(AssertionError, match="some data"):
        adapter.send(build_request(url=TEST_URL, data="unexpected data")) == response


def test_fake_adapter_with_multiple_responses():
    response_1 = fake_response(status_code=429)
    response_2 = fake_response()
    adapter = FakeAdapter(
        response_1,
        response_2,
        assertions=assert_prepared_request(url=TEST_URL, body=TEST_DATA),
    )
    request = build_request(url=TEST_URL, data=TEST_DATA)
    assert adapter.send(request) is response_1
    assert adapter.send(request) is response_2


def test_fake_adapter_with_multiple_responses_and_assertions():
    response_1 = fake_response(status_code=429)
    response_2 = fake_response()
    adapter = FakeAdapter(
        response_1,
        response_2,
        assertions=[
            assert_prepared_request(url=TEST_URL, body=TEST_DATA),
            assert_prepared_request(url=TEST_URL, body=b'{"even": "more data"}'),
        ],
    )
    request_1 = build_request(url=TEST_URL, data=TEST_DATA)
    request_2 = build_request(url=TEST_URL, json={"even": "more data"})
    assert adapter.send(request_1) is response_1
    assert adapter.send(request_2) is response_2


def test_fake_adapter_mounted_on_session():
    response = fake_response()
    adapter = FakeAdapter(response, assertions=assert_prepared_request(url=TEST_URL))
    session = Session()
    session.mount("https://", adapter)
    assert session.request("GET", TEST_URL) == response

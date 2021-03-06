import pytest
from requests import Session
from requests.adapters import BaseAdapter
from requests.models import PreparedRequest
from requtests import fake_response, FakeAdapter
from .test_utils import assert_prepared_request, build_request

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

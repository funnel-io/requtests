import pytest
from requests.models import PreparedRequest

from requtests import fake_request, fake_request_with_response, fake_response
from tests.test_utils import assert_response


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


def test_fake_request_with_assertions():
    assertions_called = False

    def assertions(prepared_request, **_):
        nonlocal assertions_called
        assertions_called = True
        assert isinstance(prepared_request, PreparedRequest)

    response = fake_response(json={"some": "data"}, status_code=418)
    fake_request(response, assertions=assertions)("get", "https://example.com")
    assert assertions_called


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


@pytest.mark.skip(reason="Pending")
def test_fake_request_with_response_with_assertions():
    pass

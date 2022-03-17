from requtests import fake_request_with_response, fake_response, fake_request
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

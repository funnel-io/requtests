from requtests import fake_response
from tests.test_utils import assert_response


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

# Requtests

![PyPI](https://img.shields.io/pypi/v/requtests)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/requtests)
![PyPI - Status](https://img.shields.io/pypi/status/requtests)
![PyPI - License](https://img.shields.io/pypi/l/requtests)
[![Python package](https://github.com/funnel-io/requtests/actions/workflows/python-package.yml/badge.svg)](https://github.com/funnel-io/requtests/actions/workflows/python-package.yml)

Test helpers for the [requests](https://docs.python-requests.org) library

## Installation

Install the package `requtests` version `1.1+` from PyPI.
The recommended `requirements.txt` line is `requtests~=1.1`.

### `FakeAdapter`

Creates an adapter intended for use with `request.Session`.
Returns the passed `Response` instance when the adapter's `send` method is called. If the `assertions` function has been specified, it will be called with the request before returning the response.

The faked adapter can be mounted using the standard `mount` method on an instance of `Session` with a suitable URL prefix. Use multiple faked adapters, specifically mounted for some URL:s, to simulate a chain of requests and responses being made.

#### Example

```python3
from requtests import FakeAdapter, fake_response
from requests import Session


class Client:
    def __init__(self):
        self.session = Session()

    def create_user(self, username):
        return self.session.post(
            "https://example.com/users",
            params={"action": "create"},
            json={"username": username},
            headers={"Authorization": "Bearer token"},
        )


def test_create_user():
    user_created_response = fake_response(json={"message": "User created!"}, status_code=201)
    adapter = FakeAdapter(user_created_response, assertions=_create_user_assertions)
    prefix = "https://example.com/users"
    
    client = Client()
    client.session.mount(prefix, adapter)
    actual_response = client.create_user("my_username")

    assert actual_response.status_code == 201
    assert actual_response.json() == {"message": "User created!"}


def _create_user_assertions(prepared_request, **kwargs):
    assert prepared_request.method == "POST"
    assert prepared_request.url == "https://example.com/users?action=create"
    assert prepared_request.headers["Authorization"] == "Bearer token"
    assert prepared_request.body == b'{"username": "my_username"}'
```

### `fake_request`

Returns a function behaving as `requests.request`, except that it returns a different response each time it is called. Useful to test e.g. pagination.

#### `fake_delete`
#### `fake_get`
#### `fake_head`
#### `fake_options`
#### `fake_patch`
#### `fake_post`
#### `fake_put`

Convenience functions returning partially applied `fake_request` functions with the HTTP `method` filled in.

### `fake_request_with_response`

Similar to `fake_request`, except that it instantiates a single `Response` object and returns it based on its arguments.

#### Example

```python3
import requests
from requtests import fake_request_with_response


def login(username, password, request_func=requests.request):
    response = request_func("POST", "https://example.com/login", data={"username": username, "password": password})
    response.raise_for_status()
    return response.json()["token"]


def test_login():
    username = "my-username"
    password = "my-password"
    request_func = fake_request_with_response(json={"token": "my-login-token"})
    assert login(username, password, request_func=request_func) == "my-login-token"

```

### `fake_response`

Returns a `requests.Response` object with either the return value of its `json()` method set to a python data structure or its `text` property set.

from functools import partial
import pytest
import requtests
from requtests import fake_response
from tests.test_utils import assert_response


@pytest.mark.parametrize(
    "func_name, method",
    {
        "fake_delete": "delete",
        "fake_get": "get",
        "fake_head": "head",
        "fake_options": "options",
        "fake_patch": "patch",
        "fake_post": "post",
        "fake_put": "put",
    }.items(),
)
def test_fake_http_method(func_name, method):
    assertions_called = False

    def assertions(prepared_request, **_):
        nonlocal assertions_called
        assertions_called = True
        assert prepared_request.method == method.upper()

    responses = [
        fake_response(json={"tea": "brewing"}, status_code=418),
        fake_response(json={"status": "I'm afraid I can't do that, Dave."}, status_code=405),
    ]

    fake_http_method = getattr(requtests, func_name)(*responses, assertions=assertions)
    assert isinstance(fake_http_method, partial)
    assert fake_http_method.args == (method,)

    assert_response(
        fake_http_method("https://api.example.com/endpoint", params={"page": 1}),
        json={"tea": "brewing"},
        status_code=418,
    )
    assert assertions_called

    assertions_called = False
    assert_response(
        fake_http_method("https://api.example.com/endpoint", params={"page": 2}),
        json={"status": "I'm afraid I can't do that, Dave."},
        status_code=405,
    )
    assert assertions_called

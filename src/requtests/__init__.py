from .fake_adapter import FakeAdapter
from .fake_request import (
    fake_delete,
    fake_get,
    fake_head,
    fake_options,
    fake_patch,
    fake_post,
    fake_put,
    fake_request,
    fake_request_with_response,
)
from .fake_response import fake_response

__all__ = [
    "FakeAdapter",
    "fake_delete",
    "fake_get",
    "fake_head",
    "fake_options",
    "fake_patch",
    "fake_post",
    "fake_put",
    "fake_request",
    "fake_request_with_response",
    "fake_response",
]
__version__ = "1.1.0"

VERSION = __version__

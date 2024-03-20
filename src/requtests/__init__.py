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
from .parsed_request import ParsedRequest

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
    "ParsedRequest",
]
__version__ = "1.2.0"

VERSION = __version__

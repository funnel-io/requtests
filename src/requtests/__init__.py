from .fake_adapter import FakeAdapter
from .fake_request import fake_request, fake_request_with_response
from .fake_response import fake_response

__all__ = [
    FakeAdapter,
    fake_request,
    fake_request_with_response,
    fake_response,
]
__version__ = "1.0.1"

VERSION = __version__

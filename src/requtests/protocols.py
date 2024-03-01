from typing import Any, Callable, List, Optional, Protocol, Union
from requests.models import PreparedRequest, Response


class AssertionFunction(Protocol):
    def __call__(self, prepared_request: PreparedRequest, **kwargs) -> Any:
        """
        An assertion function is expected to raise an error if any of its assertions fail.
        """
        pass


Assertions = Union[AssertionFunction, List[AssertionFunction]]
OptionalAssertions = Optional[Assertions]
Responder = Callable[..., Response]

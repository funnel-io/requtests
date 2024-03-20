import json
from json import JSONDecodeError
from typing import Any, Dict, List, Optional, Union
from urllib.parse import parse_qs, urlparse


class CannotParseBodyAsJSON(RuntimeError):
    def __init__(self, error):
        super().__init__(error)
        self.error = error


class ParsedRequest:
    def __init__(self, prepared_request):
        self.prepared_request = prepared_request
        self._parsed_url = urlparse(self.prepared_request.url)
        self._parsed_query = parse_qs(self._parsed_url.query)

    def __repr__(self):
        return f"<{self.__class__.__name__} [{self.method}]>"

    @property
    def body(self) -> Optional[bytes]:
        return self.prepared_request.body

    @property
    def endpoint(self) -> str:
        return f"{self._parsed_url.scheme}://{self._parsed_url.netloc}{self._parsed_url.path}"

    @property
    def headers(self) -> Dict[str, str]:
        return self.prepared_request.headers

    @property
    def json(self) -> Any:
        """
        The body of the prepared request, parsed as JSON.

        Raises a CannotParseBodyAsJSON error if the body is not valid JSON.
        """
        try:
            return json.loads(self.prepared_request.body)
        except (TypeError, JSONDecodeError) as e:
            raise CannotParseBodyAsJSON(e)

    @property
    def method(self) -> str:
        return self.prepared_request.method

    @property
    def query(self) -> Dict[str, Any]:
        return {key: _delist(value) for key, value in self._parsed_query.items()}

    @property
    def text(self) -> str:
        """
        The body of the prepared request, decoded as Unicode.
        """
        return self.prepared_request.body.decode() if self.prepared_request.body else ""

    @property
    def url(self) -> str:
        return self.prepared_request.url


def _delist(value: List[Any]) -> Union[Any, List[Any]]:
    """
    Extracts the value from a list with a single value, leaving other lists unmodifed.
    """
    return value[0] if len(value) == 1 else value

import json
from typing import Any, Dict, List, Optional, Union
from urllib.parse import parse_qs, urlparse


class ParsedRequest:
    def __init__(self, prepared_request):
        self.prepared_request = prepared_request
        self._parsed_url = urlparse(self.prepared_request.url)
        self._parsed_query = parse_qs(self._parsed_url.query)

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
        return json.loads(self.prepared_request.body)

    @property
    def method(self) -> str:
        return self.prepared_request.method

    @property
    def text(self) -> str:
        return self.prepared_request.body.decode()

    @property
    def url(self) -> str:
        return self.prepared_request.url

    @property
    def url_params(self) -> Dict[str, Any]:
        return {key: _delist(value) for key, value in self._parsed_query.items()}


def _delist(value: List[Any]) -> Union[Any, List[Any]]:
    """
    Extracts the value from a list with a single value, leaving other lists unmodifed.
    """
    return value[0] if len(value) == 1 else value

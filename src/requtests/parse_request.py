def parse_request(prepared_request):
    return ParsedRequest(prepared_request)


class ParsedRequest:
    def __init__(self, prepared_request):
        self.prepared_request = prepared_request

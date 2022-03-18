from itertools import cycle
from requests.adapters import BaseAdapter


class FakeAdapter(BaseAdapter):
    def __init__(self, *responses, assertions=None):
        super().__init__()
        self.responses = _to_generator(responses)
        self.assertions = _to_generator(assertions) if assertions else None

    def close(self):
        pass

    def send(self, request, **kwargs):
        if self.assertions:
            next(self.assertions)(request, **kwargs)
        return next(self.responses)


def _to_generator(element_or_collection):
    if _is_iterable(element_or_collection):
        return (x for x in element_or_collection)
    else:
        return cycle([element_or_collection])


def _is_iterable(obj):
    return hasattr(obj, "__iter__")

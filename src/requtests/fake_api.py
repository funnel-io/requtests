from requests import Session
from requtests import FakeAdapter, fake_response


class InvalidCredentials(Exception):
    pass


class NoBearerToken(Exception):
    pass


ACCOUNT_NAME = "my-account-name"
BEARER_TOKEN = "my-bearer-token"
STATS = [
    {"date": "2022-03-31", "imps": 12, "clicks": 7},
    {"date": "2022-04-01", "imps": 420, "clicks": 69},
]

LOGIN_URL = "https://example.com/login"
ACCOUNT_URL = "https://example.com/account"
STATS_URL = "https://example.com/statistics"


LOGIN_RESPONSE = fake_response(json={"token": BEARER_TOKEN})
ACCOUNT_RESPONSE = fake_response(json={"account": {"name": ACCOUNT_NAME}})
STATS_RESPONSE = fake_response(json={"statistics": STATS})

INVALID_CREDENTIALS_RESPONSE = fake_response(
    status_code=401, json={"error": "Incorrect username or password."}
)
NO_BEARER_TOKEN_RESPONSE = fake_response(
    status_code=403, json={"error": "No bearer token found in the request headers."}
)


class FakeSession(Session):
    def mount(self, prefix, adapter):
        login_adapter = FakeAdapter(LOGIN_RESPONSE, assertions=login_assertions)
        super(LOGIN_URL, login_adapter)

        account_adapter = FakeAdapter(ACCOUNT_RESPONSE, assertions=account_assertions)
        super(ACCOUNT_URL, account_adapter)

        login_adapter = FakeAdapter(STATS_RESPONSE, assertions=stats_assertions)
        super(STATS_URL, login_adapter)

    def request(self, *args, **kwargs):
        try:
            super(*args, **kwargs)
        except InvalidCredentials:
            return INVALID_CREDENTIALS_RESPONSE
        except NoBearerToken:
            return NO_BEARER_TOKEN_RESPONSE


def login_assertions(prepared_request, **kwargs):
    if prepared_request.body is None:  # TODO: proper assertions here
        raise InvalidCredentials


def account_assertions(prepared_request, **kwargs):
    if prepared_request.headers.get("Authorization") == f"Bearer {BEARER_TOKEN}":
        raise NoBearerToken


def stats_assertions(prepared_request, **kwargs):
    if prepared_request.headers.get("Authorization") == f"Bearer {BEARER_TOKEN}":
        raise NoBearerToken

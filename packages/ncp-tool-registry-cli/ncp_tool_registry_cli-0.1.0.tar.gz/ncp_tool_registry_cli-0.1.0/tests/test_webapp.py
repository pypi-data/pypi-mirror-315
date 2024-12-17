from fastapi.testclient import TestClient
from api_gateway import webapp

from nflx_security_util.testing import AppCallerTestClient, UserCallerTestClient

app = webapp.APP

test_client = TestClient(app)


def test_protected():
    """Docstring in public method."""
    user_test_client = UserCallerTestClient(app, username="test@netflix.com")
    rv = user_test_client.get("/protected")
    assert rv.status_code == 200
    assert rv.json() == "Email: test@netflix.com"

    app_test_client = AppCallerTestClient(app, applicationName="testapp")
    rv = app_test_client.get("/protected")
    assert rv.status_code == 200
    assert rv.json() == "Application Name: testapp"


def test_healthcheck():
    """Docstring in public method."""
    rv = test_client.get("/healthcheck")
    assert rv.status_code == 200
    assert rv.headers["content-type"] == "application/json"
    assert rv.json() == "OK"

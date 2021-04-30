import pytest

from oauth2_provider.models import Application

pytestmark = pytest.mark.django_db


def test_application_create():
    _application = Application.objects.create(
        name="Test Application",
        redirect_uris="https://example.com/redirect https://example.de/redirect",
        client_type="public",
        authorization_grant_type="authorization-code",
    )

    assert _application.name == "Test Application"

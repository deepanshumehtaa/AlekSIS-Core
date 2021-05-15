from django.conf import settings
from django.urls import reverse

import pytest

pytestmark = pytest.mark.django_db


def test_registration_page(client):
    response = client.get("/accounts/signup/")

    assert response.status_code == 200
    assert "Already have an account?" in response.content.decode("utf-8")

import re
from datetime import datetime

from django.template.loader import render_to_string
from django.utils import timezone

import pytest

from aleksis.core.models import PDFFile, Person

pytestmark = pytest.mark.django_db


def _get_test_html():
    return render_to_string("core/pages/test_pdf.html")


def test_pdf_generation():
    dummy_person = Person.objects.create(first_name="Jane", last_name="Doe")

    html = _get_test_html()
    assert "html" in html
    file_object = PDFFile.objects.create(person=dummy_person, html=html)
    assert isinstance(file_object.expires_at, datetime)
    assert file_object.expires_at > timezone.now()
    assert not bool(file_object.file)

    # generate_pdf(file_object.pk, html)

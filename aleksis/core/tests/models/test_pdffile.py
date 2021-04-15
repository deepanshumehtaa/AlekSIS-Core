import os
import re
from datetime import datetime, timedelta

from django.core.files import File
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from django.test import override_settings
from django.utils import timezone

import freezegun
import pytest

from aleksis.core.models import PDFFile, Person
from aleksis.core.util.pdf import clean_up_expired_pdf_files

pytestmark = pytest.mark.django_db


_test_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test.pdf")


def _get_test_html():
    return render_to_string("core/pages/test_pdf.html")


def test_pdf_file():
    dummy_person = Person.objects.create(first_name="Jane", last_name="Doe")

    html = _get_test_html()
    assert "html" in html
    file_object = PDFFile.objects.create(person=dummy_person, html=html)
    assert isinstance(file_object.expires_at, datetime)
    assert file_object.expires_at > timezone.now()
    assert not bool(file_object.file)

    with open(_test_pdf, "rb") as f:
        file_object.file.save("print.pdf", File(f))
    file_object.save()
    re_base = r"pdfs/print_[a-zA-Z0-9]+\.pdf"
    assert re.match(re_base, file_object.file.name)


@pytest.mark.django_db(transaction=True)
def test_delete_signal():
    dummy_person = Person.objects.create(first_name="Jane", last_name="Doe")
    file_object = PDFFile.objects.create(person=dummy_person, html=_get_test_html())
    with open(_test_pdf, "rb") as f:
        file_object.file.save("print.pdf", File(f))
    file_object.save()

    file_path = file_object.file.path

    assert default_storage.exists(file_path)
    file_object.delete()
    assert not default_storage.exists(file_path)


@pytest.mark.usefixtures("celery_worker")
@override_settings(CELERY_BROKER_URL="memory://localhost//")
@pytest.mark.django_db(transaction=True)
def test_delete_expired_files():
    # Create test instances
    dummy_person = Person.objects.create(first_name="Jane", last_name="Doe")
    file_object = PDFFile.objects.create(person=dummy_person, html=_get_test_html())
    file_object2 = PDFFile.objects.create(
        person=dummy_person, html=_get_test_html(), expires_at=timezone.now() + timedelta(hours=40)
    )
    with open(_test_pdf, "rb") as f:
        file_object.file.save("print.pdf", File(f))
        file_object2.file.save("print.pdf", File(f))
    file_object.save()
    file_object2.save()

    clean_up_expired_pdf_files()
    assert PDFFile.objects.get(pk=file_object.pk)
    assert PDFFile.objects.get(pk=file_object2.pk)

    # Prepare times
    test_time_before = timezone.now() + timedelta(hours=12)
    test_time_between = timezone.now() + timedelta(hours=30)
    test_time_after = timezone.now() + timedelta(hours=70)

    # None of the files are expired
    with freezegun.freeze_time(test_time_before):
        clean_up_expired_pdf_files()
        assert PDFFile.objects.get(pk=file_object.pk)
        assert PDFFile.objects.get(pk=file_object2.pk)

    # One file is expired
    with freezegun.freeze_time(test_time_between):
        clean_up_expired_pdf_files()
        with pytest.raises(PDFFile.DoesNotExist):
            PDFFile.objects.get(pk=file_object.pk)
        assert PDFFile.objects.get(pk=file_object2.pk)

    # Both files are expired
    with freezegun.freeze_time(test_time_after):
        clean_up_expired_pdf_files()
        with pytest.raises(PDFFile.DoesNotExist):
            PDFFile.objects.get(pk=file_object.pk)
        with pytest.raises(PDFFile.DoesNotExist):
            PDFFile.objects.get(pk=file_object2.pk)

import os
import subprocess  # noqa
from tempfile import TemporaryDirectory
from typing import Optional

from django.conf import settings
from django.core.files import File
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import gettext as _

from celery_progress.backend import ProgressRecorder

from aleksis.core.celery import app
from aleksis.core.models import PDFFile
from aleksis.core.util.celery_progress import recorded_task


@recorded_task
def generate_pdf(
    file_pk: int, html_url: str, recorder: ProgressRecorder, lang: Optional[str] = None
):
    """Generate a PDF file by rendering the HTML code using electron-pdf."""
    file_object = get_object_or_404(PDFFile, pk=file_pk)

    recorder.set_progress(0, 1)

    # Open a temporary directory
    with TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, "print.pdf")
        lang = lang or get_language()

        # Run PDF generation using a headless Chromium
        cmd = [
            "chromium",
            "--headless",
            "--no-sandbox",
            "--run-all-compositor-stages-before-draw",
            "--temp-profile",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-setuid-sandbox",
            "--dbus-stub",
            f"--home-dir={temp_dir}",
            f"--lang={lang}",
            f"--print-to-pdf={pdf_path}",
            html_url,
        ]
        res = subprocess.run(cmd)  # noqa

        # Let the task fail on a non-success return code
        res.check_returncode()

        # Upload PDF file to media storage
        with open(pdf_path, "rb") as f:
            file_object.file.save("print.pdf", File(f))
            file_object.save()

    recorder.set_progress(1, 1)


def render_pdf(request: HttpRequest, template_name: str, context: dict = None) -> HttpResponse:
    """Start PDF generation and show progress page.

    The progress page will redirect to the PDF after completion.

    .. warning::

        If celery isn't enabled, this will render the template directly in the browser.
    """
    if not context:
        context = {}

    # Generate absolute URLs for static and media files
    static_url = settings.STATIC_URL
    media_url = settings.MEDIA_URL
    if not static_url.startswith(("http://", "https://")):
        static_url = request.build_absolute_uri(static_url)
    if not media_url.startswith(("http://", "https://")):
        media_url = request.build_absolute_uri(media_url)

    with override_settings(STATIC_URL=static_url, MEDIA_URL=media_url):
        html_template = render_to_string(template_name, context)

    file_object = PDFFile.objects.create(person=request.user.person, html=html_template)
    html_url = request.build_absolute_uri(reverse("html_for_pdf_file", args=[file_object.pk]))

    result = generate_pdf.delay(file_object.pk, html_url, lang=get_language())

    redirect_url = reverse("redirect_to_pdf_file", args=[file_object.pk])

    context = {
        "title": _("Progress: Generate PDF file"),
        "back_url": context.get("back_url", "index"),
        "progress": {
            "task_id": result.task_id,
            "title": _("Generating PDF file …"),
            "success": _("The PDF file has been generated successfully."),
            "error": _("There was a problem while generating the PDF file."),
            "redirect_on_success": redirect_url,
        },
        "additional_button": {
            "href": redirect_url,
            "caption": _("Download PDF"),
            "icon": "picture_as_pdf",
        },
    }

    # Render progress view
    return render(request, "core/pages/progress.html", context)


def clean_up_expired_pdf_files() -> None:
    """Clean up expired PDF files."""
    PDFFile.objects.filter(expires_at__lt=timezone.now()).delete()


@app.task
def clean_up_expired_pdf_files_task() -> None:
    """Clean up expired PDF files."""
    return clean_up_expired_pdf_files()

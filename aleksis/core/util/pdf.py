import glob
import os
import subprocess  # noqa
from tempfile import TemporaryDirectory
from typing import Optional

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import get_language
from django.utils.translation import gettext as _

from celery_progress.backend import ProgressRecorder

from aleksis.core.celery import app
from aleksis.core.settings import MEDIA_ROOT, MEDIA_URL
from aleksis.core.util.celery_progress import recorded_task
from aleksis.core.util.core_helpers import path_and_rename


@recorded_task
def generate_pdf(
    html_code: str, pdf_path: str, recorder: ProgressRecorder, lang: Optional[str] = None
):
    """Generate a PDF file by rendering the HTML code using electron-pdf."""
    recorder.set_progress(0, 1)

    # Open a temporary directory
    with TemporaryDirectory() as temp_dir:
        # Write HTML code to a temporary file to make it available for electron-pdf
        path = os.path.join(temp_dir, "print_source.html")
        with open(path, "w") as f:
            f.write(html_code)

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
            f"file://{path}",
        ]
        subprocess.run(cmd)  # noqa

    recorder.set_progress(1, 1)


def render_pdf(request: HttpRequest, template_name: str, context: dict = None) -> HttpResponse:
    """Start PDF generation and show progress page.

    The progress page will redirect to the PDF after completion.

    .. warning::

        If celery isn't enabled, this will render the template directly in the browser.
    """
    if not context:
        context = {}
    context.setdefault("static_prefix", request.build_absolute_uri("/")[:-1])

    pdf_path = path_and_rename(None, "file.pdf", "pdfs")

    html_template = render_to_string(template_name, context)

    result = generate_pdf.delay(
        html_template, os.path.join(MEDIA_ROOT, pdf_path), lang=get_language()
    )

    context = {
        "title": _("Progress: Generate PDF file"),
        "back_url": context.get("back_url", "index"),
        "progress": {
            "task_id": result.task_id,
            "title": _("Generating PDF file …"),
            "success": _("The PDF file has been generated successfully."),
            "error": _("There was a problem while generating the PDF file."),
            "redirect_on_success": MEDIA_URL + pdf_path,
        },
        "additional_button": {
            "href": MEDIA_URL + pdf_path,
            "caption": _("Download PDF"),
            "icon": "picture_as_pdf",
        },
    }

    # Render progress view
    return render(request, "core/pages/progress.html", context)


@app.task
def clean_up_pdf_directory() -> None:
    """Clean up directory with generated PDF files."""
    files = glob.glob(os.path.join(MEDIA_ROOT, "pdfs", "*.pdf"))
    for file in files:
        os.remove(file)

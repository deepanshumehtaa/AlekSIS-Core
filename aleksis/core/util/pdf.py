import glob
import os
import subprocess  # noqa
from typing import Union

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from celery_progress.backend import ProgressRecorder

from aleksis.core.settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT
from aleksis.core.util.core_helpers import (
    DummyRecorder,
    celery_optional,
    celery_optional_progress,
    is_celery_enabled,
    make_temp_file,
    path_and_rename,
)


@celery_optional_progress
def generate_pdf(recorder: Union[ProgressRecorder, DummyRecorder], html_code: str, pdf_path: str):
    """Generate a PDF file by rendering the HTML code using electron-pdf."""
    recorder.total = 1

    # Replace /static with STATIC_ROOT to get local file system paths
    html_code = html_code.replace("/static", STATIC_ROOT)

    # Write HTML code to a temporary file to make it available for electron-pdf
    f, path = make_temp_file(".html")
    with open(path, "w") as f:
        f.write(html_code)

    subprocess.run(["electron-pdf", path, pdf_path])  # noqa

    os.remove(path)

    recorder.set_progress(1)


def render_pdf(request: HttpRequest, template_name: str, context: dict = None) -> HttpResponse:
    """Start PDF generation and show progress page.

    The progress page will redirect to the PDF after completion.

    .. warning::

        If celery isn't enabled, this will render the template directly in the browser.
    """
    if not context:
        context = {}
    pdf_path = path_and_rename(None, "file.pdf", "pdfs")

    html_template = render_to_string(template_name, context)

    if is_celery_enabled():
        result = generate_pdf(html_template, os.path.join(MEDIA_ROOT, pdf_path))

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
    else:
        # Render PaperCSS view if Celery isn't enabled
        return render(request, template_name, context)


@celery_optional
def clean_up_pdf_directory() -> None:
    """Clean up directory with generated PDF files."""
    files = glob.glob(os.path.join(MEDIA_ROOT, "pdfs", "*.pdf"))
    for file in files:
        os.remove(file)

import glob
import os
import subprocess  # noqa

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from celery_progress.backend import ProgressRecorder

from aleksis.core.celery import app
from aleksis.core.settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT
from aleksis.core.util.celery_progress import recorded_task
from aleksis.core.util.core_helpers import make_temp_file, path_and_rename


@recorded_task
def generate_pdf(html_code: str, pdf_path: str, recorder: ProgressRecorder):
    """Generate a PDF file by rendering the HTML code using electron-pdf."""
    recorder.set_progress(0, 1)

    # Replace /static with STATIC_ROOT to get local file system paths
    html_code = html_code.replace("/static", STATIC_ROOT)

    # Write HTML code to a temporary file to make it available for electron-pdf
    f, path = make_temp_file(".html")
    with open(path, "w") as f:
        f.write(html_code)

    # Start a X framebuffer and run electron-pdf
    os.environ["DISPLAY"] = ":99.0"
    xfvb_process = subprocess.Popen(  # noqa
        ["Xvfb", ":99", "-screen", "0", "1024x768x24"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(["electron-pdf", path, pdf_path])  # noqa
    xfvb_process.terminate()

    os.remove(path)

    recorder.set_progress(1, 1)


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

    result = generate_pdf.delay(html_template, os.path.join(MEDIA_ROOT, pdf_path))

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

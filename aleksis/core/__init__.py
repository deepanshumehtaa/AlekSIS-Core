import pkg_resources

from django.utils.translation import gettext_lazy as _

try:
    from .celery import app as celery_app
except ModuleNotFoundError:
    # Celery is not available
    celery_app = None

try:
    __version__ = pkg_resources.get_distribution("AlekSIS").version
except Exception:
    __version__ = "unknown"

default_app_config = "aleksis.core.apps.CoreConfig"

LICENCE_INFORMATION = {
    "name": _("Core"),
    "repository": "https://edugit.org/AlekSIS/AlekSIS/",
    "licence": _("EUPL, version 1.2 or later"),
    "copyright_holders": [
        ([2017, 2018, 2019, 2020], "Jonathan Weth", "wethjo@katharineum.de"),
        ([2017, 2018, 2019], "Frank Poetzsch-Heffter", "p-h@katharineum.de"),
        ([2018, 2019, 2020], "Hangzhi Yu", "yuha@katharineum.de"),
        ([2018, 2019, 2020], "Julian Leucker", "leuckeju@katharineum.de"),
        ([2019, 2020], "Dominik George", "dominik.george@teckids.org"),
        ([2019, 2020], "mirabilos", "thorsten.glaser@teckids.org"),
        ([2019, 2020], "Tom Teichler", "tom.teichler@teckids.org"),
    ]
}

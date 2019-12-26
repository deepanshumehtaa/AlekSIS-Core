import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("BiscuIT-ng").version
except Exception:
    __version__ = "unknown"

default_app_config = "biscuit.core.apps.CoreConfig"

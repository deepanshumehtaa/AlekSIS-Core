FROM python:3.9-buster AS core

# Configure Python to be nice inside Docker and pip to stfu
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DEFAULT_TIMEOUT 100
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1
ENV PIP_EXTRA_INDEX_URL https://edugit.org/api/v4/projects/461/packages/pypi/simple
ENV PIP_USE_DEPRECATED legacy-resolver

# Configure app settings for build and runtime
ENV ALEKSIS_static__root /usr/share/aleksis/static
ENV ALEKSIS_media__root /var/lib/aleksis/media
ENV ALEKSIS_backup__location /var/lib/aleksis/backups
ENV ALEKSIS_dev__uwsgi__celery false

# Install necessary Debian and PyPI packages for build and runtime
RUN apt-get -y update && \
    apt-get -y install eatmydata && \
    eatmydata apt-get -y upgrade && \
    eatmydata apt-get install -y --no-install-recommends \
        build-essential \
	gettext \
	libpq5 \
	libpq-dev \
	libssl-dev \
	netcat-openbsd \
	yarnpkg && \
    eatmydata pip install uwsgi django-compressor

# Install extra dependencies
ARG EXTRAS="ldap"
RUN   case ",$EXTRAS," in \
        (*",ldap,"*) \
          eatmydata apt-get install -y --no-install-recommends \
            libldap2-dev \
            libsasl2-dev \
            ldap-utils \
	  ;; \
      esac

# Install core
ARG APP_VERISON=""
RUN echo APP_VERSION="$APP_VERSION"
RUN set -e; \
    mkdir -p /var/lib/aleksis/media /usr/share/aleksis/static /var/lib/aleksis/backups; \
    eatmydata pip install AlekSIS-Core\[$EXTRAS\]$APP_VERSION

# Declare a persistent volume for all data
VOLUME /var/lib/aleksis

# Define entrypoint and uWSGI running on port 8000
EXPOSE 8000
COPY docker-entrypoint.sh /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Install assets
FROM core as assets
RUN eatmydata aleksis-admin yarn install

# Clean up build dependencies
FROM assets AS clean
RUN set -e; \
    eatmydata apt-get remove --purge -y \
        build-essential \
        gettext \
        libpq-dev \
        libssl-dev \
        libldap2-dev \
        libsasl2-dev \
        yarnpkg; \
    eatmydata apt-get autoremove --purge -y; \
    apt-get clean -y; \
    rm -f /var/lib/apt/lists/*_*; \
    rm -rf /root/.cache

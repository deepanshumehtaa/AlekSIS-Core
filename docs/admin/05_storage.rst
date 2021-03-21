Storage
##########

Amazon S3
*********

AlekSIS allows you to configure an Amazon S3 endpoint for static and media
files. This is useful e.g. for loadbalancing with multiple AlekSIS
instances.

Configure a S3 endpoint
=======================

If you want to use a S3 endpoint to store files you have to configure the
endpoint in your configfile (`/etc/aleksis/aleksis.toml`)::

  # Default values
  [storage.s3]
  region = ""
  access_key_id = ""
  session_token = ""
  bucket_name = ""
  addressing_style = ""
  endpoint_url = ""
  key_prefix = ""
  bucket_auth = true
  max_age_seconds = 3600 # 1 hour
  max_age_seconds_cached_static = 31536000 # 24 hours
  public_url = ""
  reduced_redundancy = false
  content_disposition = ""
  content_language = ""
  metadata = {}
  encrypt_key = False
  kms_encryption_key_id = ""
  gzip = true
  signature_version = None
  file_overwrite = false

For more information please see https://pypi.org/project/django-s3-storage/

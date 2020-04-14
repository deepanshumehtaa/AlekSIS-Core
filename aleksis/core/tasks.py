from django.apps import apps
from geopy.geocoders import OpenMapQuest
from geopy.geocoders.base import GeocoderServiceError

from .util.core_helpers import celery_optional
from .util.notifications import send_notification as _send_notification


@celery_optional
def send_notification(notification: int, resend: bool = False) -> None:
    _send_notification(notification, resend)


@celery_optional
def update_coordinates() -> None:
    """ Update coordinates if postal address is given  """

    if config.ENABLE_GEOLOCATION_OF_PERSONS:

        # Get person model
        Person = apps.get_model("core", "Person")

        # Get API key from settings
        nominatim = OpenMapQuest(api_key=getattr(config, "MAPQUEST_API_KEY", None),
                         user_agent="AlekSIS")

        for person in Person.objects.all():
            if person.full_address:
                try:
                    location = nominatim.geocode(person.full_address)
                except GeocoderServiceError:
                    location = None

                if location:
                    person.latitude, person.longitude = location.latitude, location.longitude

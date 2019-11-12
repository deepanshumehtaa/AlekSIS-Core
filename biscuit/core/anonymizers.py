import requests

from django.core.files.base import ContentFile
from hattori.base import BaseAnonymizer, faker

from .models import Person


def get_photo(**kwargs):
    req = requests.get(
        'https://thispersondoesnotexist.com/image',
        headers={
            'User-Agent': faker.firefox()
        }
    )

    # Needed to get around hattori trying to truncate to max_length
    class _ContentFile(ContentFile):
        def __getitem__(self, key):
            return self

    return _ContentFile(req.content, faker.file_name(extension='jpg'))


class PersonAnonymizer(BaseAnonymizer):
    model = Person

    attributes = [
        ('first_name', faker.first_name),
        ('last_name', faker.last_name),
        ('additional_name', ''),
        ('short_name', lambda **kwargs: faker.pystr(min_chars=3, max_chars=5, **kwargs)),
        ('street', faker.street_name),
        ('housenumber', faker.building_number),
        ('postal_code', faker.postcode),
        ('place', faker.city),
        ('phone_number', ''),
        ('mobile_number', ''),
        ('email', faker.email),
        ('date_of_birth', lambda **kwargs: faker.date_of_birth(minimum_age=8, maximum_age=66, **kwargs)),
        ('photo', get_photo)
    ]

from urllib.request import Request, urlopen

from hattori.base import BaseAnonymizer, faker

from .models import Person


def get_photo(**kwargs):
    req = Request(
        'https://thispersondoesnotexist.com/image',
        data=None,
        headers={
            'User-Agent': faker.firefox()
        }
    )
    return urlopen(req).read()


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

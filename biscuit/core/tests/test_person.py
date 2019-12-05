from django.test import TestCase

from biscuit.core.models import Person


class PersonTestCase(TestCase):
    def setUp(self):
        self._person = Person.objects.create(
            first_name='Jane',
            last_name='Doe'
        )

    def test_full_name(self):
        assert self._person.full_name == 'Doe, Jane'

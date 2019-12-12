import pytest

from biscuit.core.models import Person


@pytest.mark.django_db
def test_full_name():
    _person = Person.objects.create(first_name='Jane', last_name='Doe')

    assert _person.full_name == 'Doe, Jane'

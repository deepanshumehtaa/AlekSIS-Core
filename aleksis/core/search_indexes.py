from .models import Person, Group
from .util.search import Indexable, SearchIndex


class PersonIndex(SearchIndex, Indexable):
    model = Person


class GroupIndex(SearchIndex, Indexable):
    model = Group

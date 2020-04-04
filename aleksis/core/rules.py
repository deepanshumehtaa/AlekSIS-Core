
from rules import predicate, add_perm

from aleksis.core.util.core_helpers import has_person

print("rules?")

@predicate
def has_person_predicate(user):
    # return has_person(user)
    return True

add_perm('core.view_person', has_person_predicate)
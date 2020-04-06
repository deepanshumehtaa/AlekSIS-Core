from rules import add_perm, always_allow

from aleksis.core.models import Person
from aleksis.core.util.predicates import (
    has_person_predicate,
    has_global_perm,
    has_any_object,
    is_person,
    has_object_perm,
)


add_perm("core", always_allow)

# View persons
view_persons_predicate = has_person_predicate & (
    has_global_perm("core.view_person") | has_any_object("core.view_person", Person)
)
add_perm("core.view_persons", view_persons_predicate)

# View person
view_person_predicate = has_person_predicate & (
    has_global_perm("core.view_person") | has_object_perm("core.view_person") | is_person
)
add_perm("core.view_person", view_person_predicate)

# Change person
change_person_predicate = has_person_predicate & (
    has_global_perm("core.change_person") | has_object_perm("core.change_person")
)
add_perm("core.change_person", change_person_predicate)

# People menu (persons + objects)
add_perm("core.view_people_menu", has_person_predicate & (view_persons_predicate))

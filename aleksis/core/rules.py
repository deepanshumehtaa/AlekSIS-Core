from rules import add_perm, always_allow

from aleksis.core.models import Person, Group
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

# View person address
view_address_predicate = has_person_predicate & (
    has_global_perm("core.view_address") | has_object_perm("core.view_address") | is_person
)
add_perm("core.view_address", view_address_predicate)

# View person contact details
view_contact_details_predicate = has_person_predicate & (
    has_global_perm("core.view_contact_details") | has_object_perm("core.view_contact_details") | is_person
)
add_perm("core.view_contact_details", view_contact_details_predicate)

# View person photo
view_photo_predicate = has_person_predicate & (
    has_global_perm("core.view_photo") | has_object_perm("core.view_photo") | is_person
)
add_perm("core.view_photo", view_photo_predicate)

# Change person
change_person_predicate = has_person_predicate & (
    has_global_perm("core.change_person") | has_object_perm("core.change_person")
)
add_perm("core.change_person", change_person_predicate)

# View groups
view_groups_predicate = has_person_predicate & (
    has_global_perm("core.view_group") | has_any_object("core.view_group", Group)
)
add_perm("core.view_groups", view_groups_predicate)

# View group
view_group_predicate = has_person_predicate & (
    has_global_perm("core.view_group") | has_object_perm("core.view_group")
)
add_perm("core.view_group", view_group_predicate)

# People menu (persons + objects)
add_perm("core.view_people_menu", has_person_predicate & (view_persons_predicate | view_groups_predicate))

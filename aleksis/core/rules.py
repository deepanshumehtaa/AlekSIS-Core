from rules import add_perm, always_allow

from aleksis.core.models import Person, Group, Announcement
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

# View persons groups
view_groups_predicate = has_person_predicate & (
    has_global_perm("core.view_person_groups") | has_object_perm("core.view_person_groups") | is_person
)
add_perm("core.view_person_groups", view_groups_predicate)

# Edit person
edit_person_predicate = has_person_predicate & (
    has_global_perm("core.change_person") | has_object_perm("core.change_person")
)
add_perm("core.edit_person", edit_person_predicate)

# Link persons with accounts
link_persons_accounts_predicate = has_person_predicate & has_global_perm("core.link_persons_accounts")
add_perm("core.link_persons_accounts", link_persons_accounts_predicate)

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

# Edit group
edit_group_predicate = has_person_predicate & (
    has_global_perm("core.change_group") | has_object_perm("core.change_group")
)
add_perm("core.edit_group", edit_group_predicate)

# Edit school information
edit_school_information_predicate = has_person_predicate & has_global_perm("core.change_school")
add_perm("core.edit_school_information", edit_school_information_predicate)

# Edit school term
edit_schoolterm_predicate = has_person_predicate & has_global_perm("core.change_schoolterm")
add_perm("core.edit_schoolterm", edit_schoolterm_predicate)

# Manage school
manage_school_predicate = edit_school_information_predicate | edit_schoolterm_predicate
add_perm("core.manage_school", manage_school_predicate)

# Manage data
manage_data_predicate = has_person_predicate & has_global_perm("core.manage_data")
add_perm("core.manage_data", manage_data_predicate)

# View announcements
view_announcements_predicate = has_person_predicate & (
    has_global_perm("core.view_announcements") | has_any_object("core.view_announcements", Announcement)
)
add_perm("core.view_announcements", view_announcements_predicate)

# Create or edit announcements
create_or_edit_announcement_predicate = has_person_predicate & (
    has_global_perm("core.create_or_edit_announcement") | has_object_perm("core.create_or_edit_announcement")
)
add_perm("core.create_or_edit_announcement", create_or_edit_announcement_predicate)

# Delete announcement
delete_announcement_predicate = has_person_predicate & (
    has_global_perm("core.delete_announcement") | has_object_perm("core.delete_announcement")
)
add_perm("core.delete_announcement", delete_announcement_predicate)

# View people menu (persons + objects)
add_perm("core.view_people_menu", has_person_predicate & (view_persons_predicate | view_groups_predicate))

# View system status
view_system_status_predicate = has_person_predicate & has_global_perm("core.view_system_status")
add_perm("core.view_system_status", view_system_status_predicate)

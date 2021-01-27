from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .util.core_helpers import unread_notifications_badge

MENUS = {
    "NAV_MENU_CORE": [
        {
            "name": _("Login"),
            "url": settings.LOGIN_URL,
            "icon": "lock_open",
            "validators": ["menu_generator.validators.is_anonymous"],
        },
        {
            "name": _("Dashboard"),
            "url": "index",
            "icon": "home",
            "validators": ["menu_generator.validators.is_authenticated"],
        },
        {
            "name": _("Notifications"),
            "url": "notifications",
            "icon": "notifications",
            "badge": unread_notifications_badge,
            "validators": [
                ("aleksis.core.util.predicates.permission_validator", "core.view_notifications",),
            ],
        },
        {
            "name": _("Account"),
            "url": "#",
            "icon": "person",
            "related_urls": [
                "twofactor:profile",
                "twofactor:setup",
                "twofactor:setup_complete",
                "twofactor:backup_tokens",
                "twofactor:phone_create",
                "twofactor:phone_delete",
                "twofactor:disable",
                "person",
            ],
            "root": True,
            "validators": ["menu_generator.validators.is_authenticated"],
            "submenu": [
                {
                    "name": _("Stop impersonation"),
                    "url": "impersonate-stop",
                    "icon": "stop",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "aleksis.core.util.core_helpers.is_impersonate",
                    ],
                },
                {
                    "name": _("Logout"),
                    "url": "logout",
                    "icon": "exit_to_app",
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
                {
                    "name": _("2FA"),
                    "url": "two_factor:profile",
                    "icon": "phonelink_lock",
                    "related_urls": [
                        "twofactor:profile",
                        "twofactor:setup",
                        "twofactor:setup_complete",
                        "twofactor:backup_tokens",
                        "twofactor:phone_create",
                        "twofactor:phone_delete",
                        "twofactor:disable",
                    ],
                    "validators": ["menu_generator.validators.is_authenticated",],
                },
                {
                    "name": _("Me"),
                    "url": "person",
                    "icon": "insert_emoticon",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "aleksis.core.util.core_helpers.has_person",
                    ],
                },
                {
                    "name": _("Preferences"),
                    "url": "preferences_person",
                    "icon": "settings",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "aleksis.core.util.core_helpers.has_person",
                    ],
                },
            ],
        },
        {
            "name": _("Admin"),
            "url": "#",
            "icon": "security",
            "related_urls": [
                "announcements",
                "add_announcement",
                "edit_announcement",
                "delete_announcement",
                "preferences_site",
                "dashboard_widgets",
                "school_terms",
                "create_school_term",
                "edit_school_term",
                "check_data",
                "data_check_run",
                "data_check_solve",
            ],
            "validators": [
                ("aleksis.core.util.predicates.permission_validator", "core.view_admin_menu"),
            ],
            "submenu": [
                {
                    "name": _("Announcements"),
                    "url": "announcements",
                    "icon": "announcement",
                    "related_urls": [
                        "announcements",
                        "add_announcement",
                        "edit_announcement",
                        "delete_announcement",
                    ],
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.view_announcements",
                        ),
                    ],
                },
                {
                    "name": _("School terms"),
                    "url": "school_terms",
                    "icon": "date_range",
                    "related_urls": ["school_terms", "create_school_term", "edit_school_term"],
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.view_schoolterm",
                        ),
                    ],
                },
                {
                    "name": _("Dashboard widgets"),
                    "url": "dashboard_widgets",
                    "icon": "dashboard",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.view_dashboardwidget",
                        ),
                    ],
                },
                {
                    "name": _("Data management"),
                    "url": "data_management",
                    "icon": "view_list",
                    "validators": [
                        ("aleksis.core.util.predicates.permission_validator", "core.manage_data"),
                    ],
                },
                {
                    "name": _("System status"),
                    "url": "system_status",
                    "icon": "power_settings_new",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.view_system_status",
                        ),
                    ],
                },
                {
                    "name": _("Impersonation"),
                    "url": "impersonate-list",
                    "icon": "people",
                    "validators": [
                        ("aleksis.core.util.predicates.permission_validator", "core.impersonate"),
                    ],
                },
                {
                    "name": _("Configuration"),
                    "url": "preferences_site",
                    "icon": "settings",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.change_site_preferences",
                        ),
                    ],
                },
                {
                    "name": _("Data checks"),
                    "url": "check_data",
                    "icon": "done_all",
                    "related_urls": ["check_data", "data_check_run", "data_check_solve"],
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": _("Backend Admin"),
                    "url": "admin:index",
                    "icon": "settings",
                    "validators": ["menu_generator.validators.is_superuser",],
                },
            ],
        },
        {
            "name": _("People"),
            "url": "#",
            "icon": "people",
            "root": True,
            "related_urls": [
                "persons",
                "edit_person",
                "create_person",
                "person_by_id",
                "edit_person_by_id",
                "delete_person_by_id",
                "groups",
                "group_by_id",
                "edit_group_by_id",
                "delete_group_by_id",
                "create_group_type",
                "edit_group_type_by_id",
                "delete_group_type_by_id",
                "group_types",
                "additional_fields",
                "groups_child_groups",
                "edit_additional_field_by_id",
                "create_additional_field",
                "delete_additional_field_by_id",
                "create_group",
            ],
            "validators": [
                ("aleksis.core.util.predicates.permission_validator", "core.view_people_menu")
            ],
            "submenu": [
                {
                    "name": _("Persons"),
                    "url": "persons",
                    "icon": "person",
                    "related_urls": [
                        "persons",
                        "edit_person",
                        "create_person",
                        "person_by_id",
                        "edit_person_by_id",
                        "delete_person_by_id",
                    ],
                    "validators": [
                        ("aleksis.core.util.predicates.permission_validator", "core.view_persons")
                    ],
                },
                {
                    "name": _("Groups"),
                    "url": "groups",
                    "icon": "group",
                    "related_urls": [
                        "groups",
                        "group_by_id",
                        "edit_group_by_id",
                        "delete_group_by_id",
                        "create_group",
                    ],
                    "validators": [
                        ("aleksis.core.util.predicates.permission_validator", "core.view_groups")
                    ],
                },
                {
                    "name": _("Group types"),
                    "url": "group_types",
                    "icon": "category",
                    "related_urls": [
                        "edit_group_type_by_id",
                        "delete_group_type_by_id",
                        "group_types",
                    ],
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.view_group_type",
                        )
                    ],
                },
                {
                    "name": _("Persons and accounts"),
                    "url": "persons_accounts",
                    "icon": "person_add",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.link_persons_accounts",
                        )
                    ],
                },
                {
                    "name": _("Groups and child groups"),
                    "url": "groups_child_groups",
                    "icon": "group_add",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.assign_child_groups_to_groups",
                        )
                    ],
                },
                {
                    "name": _("Additional fields"),
                    "url": "additional_fields",
                    "related_urls": [
                        "additional_fields",
                        "edit_additional_field_by_id",
                        "create_additional_field",
                        "delete_additional_field_by_id",
                    ],
                    "icon": "style",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.view_additionalfield",
                        )
                    ],
                },
            ],
        },
    ],
    "DATA_MANAGEMENT_MENU": [
        {
            "name": _("Assign child groups to groups"),
            "url": "groups_child_groups",
            "validators": [
                (
                    "aleksis.core.util.predicates.permission_validator",
                    "core.assign_child_groups_to_groups",
                )
            ],
        },
    ],
}

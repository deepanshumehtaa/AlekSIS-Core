from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .util.core_helpers import unread_notifications_badge

MENUS = {
    "NAV_MENU_CORE": [
        {
            "name": _("Login"),
            "url": settings.LOGIN_URL,
            "svg_icon": "mdi:login-variant",
            "validators": ["menu_generator.validators.is_anonymous"],
        },
        {
            "name": _("Sign up"),
            "url": "account_signup",
            "svg_icon": "mdi:account-plus-outline",
            "validators": [
                "menu_generator.validators.is_anonymous",
                ("aleksis.core.util.predicates.permission_validator", "core.can_register"),
            ],
        },
        {
            "name": _("Dashboard"),
            "url": "index",
            "svg_icon": "mdi:home-outline",
            "validators": [
                ("aleksis.core.util.predicates.permission_validator", "core.view_dashboard_rule")
            ],
        },
        {
            "name": _("Notifications"),
            "url": "notifications",
            "svg_icon": "mdi:bell-outline",
            "badge": unread_notifications_badge,
            "validators": [
                ("aleksis.core.util.predicates.permission_validator", "core.view_notifications",),
            ],
        },
        {
            "name": _("Account"),
            "url": "#",
            "svg_icon": "mdi:account-outline",
            "root": True,
            "validators": ["menu_generator.validators.is_authenticated"],
            "submenu": [
                {
                    "name": _("Stop impersonation"),
                    "url": "impersonate-stop",
                    "svg_icon": "mdi:stop",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "aleksis.core.util.core_helpers.is_impersonate",
                    ],
                },
                {
                    "name": _("Logout"),
                    "url": "logout",
                    "svg_icon": "mdi:logout-variant",
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
                {
                    "name": _("2FA"),
                    "url": "two_factor:profile",
                    "svg_icon": "mdi:two-factor-authentication",
                    "validators": ["menu_generator.validators.is_authenticated",],
                },
                {
                    "name": _("Change password"),
                    "url": "account_change_password",
                    "svg_icon": "mdi:form-textbox-password",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.can_change_password",
                        ),
                    ],
                },
                {
                    "name": _("Me"),
                    "url": "person",
                    "svg_icon": "mdi:emoticon-outline",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "aleksis.core.util.core_helpers.has_person",
                    ],
                },
                {
                    "name": _("Preferences"),
                    "url": "preferences_person",
                    "svg_icon": "mdi:cog-outline",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "aleksis.core.util.core_helpers.has_person",
                    ],
                },
                {
                    "name": _("Third-party accounts"),
                    "url": "socialaccount_connections",
                    "svg_icon": "mdi:earth",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "aleksis.core.util.core_helpers.has_person",
                    ],
                },
                {
                    "name": _("Authorized applications"),
                    "url": "oauth2_provider:authorized-token-list",
                    "svg_icon": "mdi:gesture-tap-hold",
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
            "svg_icon": "mdi:security",
            "validators": [
                ("aleksis.core.util.predicates.permission_validator", "core.view_admin_menu"),
            ],
            "submenu": [
                {
                    "name": _("Announcements"),
                    "url": "announcements",
                    "svg_icon": "mdi:message-alert-outline",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.view_announcements_rule",
                        ),
                    ],
                },
                {
                    "name": _("School terms"),
                    "url": "school_terms",
                    "svg_icon": "mdi:calendar-range-outline",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.view_schoolterm_rule",
                        ),
                    ],
                },
                {
                    "name": _("Dashboard widgets"),
                    "url": "dashboard_widgets",
                    "svg_icon": "mdi:view-dashboard-outline",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.view_dashboardwidget_rule",
                        ),
                    ],
                },
                {
                    "name": _("Data management"),
                    "url": "data_management",
                    "svg_icon": "mdi:chart-donut",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.manage_data_rule",
                        ),
                    ],
                },
                {
                    "name": _("System status"),
                    "url": "system_status",
                    "svg_icon": "mdi:power-settings",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.view_system_status_rule",
                        ),
                    ],
                },
                {
                    "name": _("Impersonation"),
                    "url": "impersonate-list",
                    "svg_icon": "mdi:account-switch-outline",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.impersonate_rule",
                        ),
                    ],
                },
                {
                    "name": _("Configuration"),
                    "url": "preferences_site",
                    "svg_icon": "mdi:tune",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.change_site_preferences_rule",
                        ),
                    ],
                },
                {
                    "name": _("Data checks"),
                    "url": "check_data",
                    "svg_icon": "mdi:list-status",
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": _("Backend Admin"),
                    "url": "admin:index",
                    "svg_icon": "mdi:database-cog-outline",
                    "validators": ["menu_generator.validators.is_superuser",],
                },
                {
                    "name": _("OAuth2 Applications"),
                    "url": "oauth_list",
                    "svg_icon": "mdi:gesture-tap-hold",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.list_oauth_applications_rule",
                        ),
                    ],
                },
            ],
        },
        {
            "name": _("People"),
            "url": "#",
            "svg_icon": "mdi:account-group-outline",
            "root": True,
            "validators": [
                ("aleksis.core.util.predicates.permission_validator", "core.view_people_menu_rule")
            ],
            "submenu": [
                {
                    "name": _("Persons"),
                    "url": "persons",
                    "svg_icon": "mdi:account-outline",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.view_persons_rule",
                        )
                    ],
                },
                {
                    "name": _("Groups"),
                    "url": "groups",
                    "svg_icon": "mdi:account-multiple-outline",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.view_groups_rule",
                        )
                    ],
                },
                {
                    "name": _("Group types"),
                    "url": "group_types",
                    "svg_icon": "mdi:shape-outline",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.view_grouptypes_rule",
                        )
                    ],
                },
                {
                    "name": _("Persons and accounts"),
                    "url": "persons_accounts",
                    "svg_icon": "mdi:account-plus-outline",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.link_persons_accounts_rule",
                        )
                    ],
                },
                {
                    "name": _("Groups and child groups"),
                    "url": "groups_child_groups",
                    "svg_icon": "mdi:account-multiple-plus-outline",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.assign_child_groups_to_groups_rule",
                        )
                    ],
                },
                {
                    "name": _("Additional fields"),
                    "url": "additional_fields",
                    "svg_icon": "mdi:palette-swatch-outline",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "core.view_additionalfields_rule",
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
                    "core.assign_child_groups_to_groups_rule",
                )
            ],
        },
    ],
}
